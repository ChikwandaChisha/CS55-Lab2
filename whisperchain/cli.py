#!/usr/bin/env python3
import argparse
import sys
from auth.register import register_user, login_user
from tokens.generate import generate_token
from messaging.send import send_message, get_receiver_messages, mark_message_read
from messaging.flag import flag_message
from rbac.access_control import check_permission
from logging.audit import log_event

def main():
    parser = argparse.ArgumentParser(description='WhisperChain+ CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Register command
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('--username', required=True, help='Username')
    register_parser.add_argument('--password', required=True, help='Password')
    register_parser.add_argument('--role', required=True, choices=['Sender', 'Receiver', 'Moderator'], help='User role')
    register_parser.add_argument('--email', required=True, help='Dartmouth email address (@dartmouth.edu)')

    # Login command
    login_parser = subparsers.add_parser('login', help='Login to the system')
    login_parser.add_argument('--username', required=True, help='Username')
    login_parser.add_argument('--password', required=True, help='Password')

    # Get token command
    token_parser = subparsers.add_parser('get-token', help='Get an anonymous token')
    token_parser.add_argument('--username', required=True, help='Username')
    token_parser.add_argument('--password', required=True, help='Password')

    # Send message command
    send_parser = subparsers.add_parser('send', help='Send a message')
    send_parser.add_argument('--username', required=True, help='Username')
    send_parser.add_argument('--password', required=True, help='Password')
    send_parser.add_argument('--token', required=True, help='Anonymous token')
    send_parser.add_argument('--message', required=True, help='Message content')
    send_parser.add_argument('--receiver', required=True, help='Receiver username')

    # View messages command
    view_parser = subparsers.add_parser('view', help='View messages')
    view_parser.add_argument('--username', required=True, help='Username')
    view_parser.add_argument('--password', required=True, help='Password')
    view_parser.add_argument('--mark-read', action='store_true', help='Mark messages as read')

    # Flag message command
    flag_parser = subparsers.add_parser('flag', help='Flag a message')
    flag_parser.add_argument('--username', required=True, help='Username')
    flag_parser.add_argument('--password', required=True, help='Password')
    flag_parser.add_argument('--message-id', required=True, help='Message ID to flag')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'register':
            register_user(args.username, args.password, args.role, args.email)
            log_event('registration', {'username': args.username, 'role': args.role, 'email': args.email})
            print(f"User {args.username} registered successfully!")

        elif args.command == 'login':
            if login_user(args.username, args.password):
                log_event('login', {'username': args.username})
                print(f"Welcome back, {args.username}!")
            else:
                print("Invalid credentials!")
                sys.exit(1)

        elif args.command == 'get-token':
            if not check_permission(args.username, 'get_token'):
                print("Permission denied: Only Senders can get tokens")
                sys.exit(1)
            token = generate_token(args.username)
            log_event('token_generation', {'username': args.username})
            print(f"Your anonymous token: {token}")

        elif args.command == 'send':
            if not check_permission(args.username, 'send_message'):
                print("Permission denied: Only Senders can send messages")
                sys.exit(1)
            message_id = send_message(args.username, args.token, args.message, args.receiver)
            log_event('message_sent', {'username': args.username, 'message_id': message_id, 'receiver': args.receiver})
            print(f"Message sent successfully! (ID: {message_id})")

        elif args.command == 'view':
            if not check_permission(args.username, 'view_messages'):
                print("Permission denied: Only Receivers can view messages")
                sys.exit(1)
            
            messages = get_receiver_messages(args.username)
            if not messages:
                print("No messages available.")
            else:
                print("\nYour messages:")
                for msg in messages:
                    status = "✓" if msg['read'] else "✗"
                    flagged = "🚩" if msg['flagged'] else ""
                    print(f"\n{status} Message ID: {msg['message_id']} {flagged}")
                    print(f"Content: {msg['content']}")
                    print(f"Received: {msg['received_at']}")
                    
                    if args.mark_read and not msg['read']:
                        mark_message_read(args.username, msg['message_id'])
                        print("(Marked as read)")
            
            log_event('messages_viewed', {'username': args.username})

        elif args.command == 'flag':
            if not check_permission(args.username, 'flag_message'):
                print("Permission denied: Only Moderators can flag messages")
                sys.exit(1)
            flag_id = flag_message(args.username, args.message_id)
            log_event('message_flagged', {'username': args.username, 'message_id': args.message_id})
            print(f"Message flagged successfully! (Flag ID: {flag_id})")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 