"""
Enhanced routes for social network features
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func, join
from typing import List, Optional
from datetime import datetime, timedelta
from main import (
    get_db, get_current_user, User, Post, Friendship, 
    Notification, Follow, Block, manager, Reaction
)
import json

router = APIRouter()

# Enhanced user discovery and search
@router.get("/users/discover")
async def discover_users(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    limit: int = Query(default=20, le=50)
):
    """Descobrir novos usuários para seguir/adicionar"""
    
    # Get users that are not friends and not blocked
    existing_friends = db.query(Friendship.addressee_id, Friendship.requester_id).filter(
        or_(
            Friendship.requester_id == current_user.id,
            Friendship.addressee_id == current_user.id
        ),
        Friendship.status == "accepted"
    ).all()
    
    friend_ids = set()
    for friendship in existing_friends:
        friend_ids.add(friendship.addressee_id if friendship.requester_id == current_user.id else friendship.requester_id)
    
    # Get blocked users
    blocked_users = db.query(Block.blocked_id).filter(Block.blocker_id == current_user.id).all()
    blocked_ids = {block.blocked_id for block in blocked_users}
    
    # Exclude current user, friends, and blocked users
    exclude_ids = friend_ids.union(blocked_ids).union({current_user.id})
    
    users = db.query(User).filter(
        User.is_active == True,
        ~User.id.in_(exclude_ids) if exclude_ids else True
    ).order_by(User.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "bio": user.bio,
            "avatar": user.avatar,
            "location": user.location,
            "mutual_friends": 0  # TODO: Calculate mutual friends
        }
        for user in users
    ]

# User statistics
@router.get("/users/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Estatísticas do usuário"""
    
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate stats
    posts_count = db.query(Post).filter(Post.author_id == user_id).count()
    
    friends_count = db.query(Friendship).filter(
        or_(
            and_(Friendship.requester_id == user_id, Friendship.status == "accepted"),
            and_(Friendship.addressee_id == user_id, Friendship.status == "accepted")
        )
    ).count()
    
    # Total reactions received
    reactions_received = db.query(func.count(Reaction.id)).select_from(
        join(Post, Reaction, Post.id == Reaction.post_id)
    ).filter(Post.author_id == user_id).scalar() or 0
    
    return {
        "user_id": user_id,
        "posts_count": posts_count,
        "friends_count": friends_count,
        "reactions_received": reactions_received,
        "member_since": user.created_at,
        "last_seen": user.last_seen
    }

# User blocking functionality
@router.post("/users/{user_id}/block")
async def block_user(
    user_id: int,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Bloquear usuário"""
    
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
    
    # Check if user exists
    user_to_block = db.query(User).filter(User.id == user_id).first()
    if not user_to_block:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already blocked
    existing_block = db.query(Block).filter(
        Block.blocker_id == current_user.id,
        Block.blocked_id == user_id
    ).first()
    
    if existing_block:
        raise HTTPException(status_code=400, detail="User already blocked")
    
    # Remove friendship if exists
    friendship = db.query(Friendship).filter(
        or_(
            and_(Friendship.requester_id == current_user.id, Friendship.addressee_id == user_id),
            and_(Friendship.requester_id == user_id, Friendship.addressee_id == current_user.id)
        )
    ).first()
    
    if friendship:
        db.delete(friendship)
    
    # Create block
    new_block = Block(
        blocker_id=current_user.id,
        blocked_id=user_id
    )
    db.add(new_block)
    db.commit()
    
    return {"message": "User blocked successfully"}

@router.delete("/users/{user_id}/block")
async def unblock_user(
    user_id: int,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Desbloquear usuário"""
    
    block = db.query(Block).filter(
        Block.blocker_id == current_user.id,
        Block.blocked_id == user_id
    ).first()
    
    if not block:
        raise HTTPException(status_code=404, detail="User is not blocked")
    
    db.delete(block)
    db.commit()
    
    return {"message": "User unblocked successfully"}

@router.get("/users/blocked")
async def get_blocked_users(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Listar usuários bloqueados"""
    
    blocked = db.query(Block).filter(Block.blocker_id == current_user.id).all()
    
    blocked_users = []
    for block in blocked:
        user = db.query(User).filter(User.id == block.blocked_id).first()
        if user:
            blocked_users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "avatar": user.avatar,
                "blocked_at": block.created_at
            })
    
    return blocked_users

# Enhanced activity feed
@router.get("/feed/activity")
async def get_activity_feed(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    limit: int = Query(default=20, le=50)
):
    """Feed de atividades dos amigos"""
    
    # Get friends
    friends = db.query(Friendship).filter(
        or_(
            and_(Friendship.requester_id == current_user.id, Friendship.status == "accepted"),
            and_(Friendship.addressee_id == current_user.id, Friendship.status == "accepted")
        )
    ).all()
    
    friend_ids = []
    for friendship in friends:
        friend_id = friendship.addressee_id if friendship.requester_id == current_user.id else friendship.requester_id
        friend_ids.append(friend_id)
    
    # Include current user's posts too
    friend_ids.append(current_user.id)
    
    # Get recent posts from friends
    posts = db.query(Post).filter(
        Post.author_id.in_(friend_ids),
        Post.created_at >= datetime.utcnow() - timedelta(days=30)  # Last 30 days
    ).order_by(Post.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": post.id,
            "author": {
                "id": post.author.id,
                "first_name": post.author.first_name,
                "last_name": post.author.last_name,
                "avatar": post.author.avatar
            },
            "content": post.content,
            "post_type": post.post_type,
            "media_type": post.media_type,
            "media_url": post.media_url,
            "created_at": post.created_at,
            "reactions_count": post.reactions_count,
            "comments_count": post.comments_count,
            "shares_count": post.shares_count
        }
        for post in posts
    ]

# Enhanced notification management
@router.get("/notifications/recent")
async def get_recent_notifications(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
    limit: int = Query(default=10, le=50)
):
    """Notificações recentes (últimas 24h)"""
    
    since = datetime.utcnow() - timedelta(hours=24)
    
    notifications = db.query(Notification).filter(
        Notification.recipient_id == current_user.id,
        Notification.created_at >= since
    ).order_by(Notification.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": notification.id,
            "type": notification.notification_type,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
            "sender": {
                "id": notification.sender.id,
                "name": f"{notification.sender.first_name} {notification.sender.last_name}",
                "avatar": notification.sender.avatar
            } if notification.sender else None
        }
        for notification in notifications
    ]
