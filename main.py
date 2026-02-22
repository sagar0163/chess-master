#!/usr/bin/env python3
"""
Chess Master - Main Entry Point
================================
"""

import sys
from game import ChessGame


def main():
    """Main entry point"""
    ai_enabled = '--no-ai' not in sys.argv
    ai_depth = 3
    
    for arg in sys.argv:
        if arg.startswith('--depth='):
            try:
                ai_depth = int(arg.split('=')[1])
            except ValueError:
                pass
    
    game = ChessGame(ai_enabled=ai_enabled, ai_depth=ai_depth)
    game.start()


if __name__ == '__main__':
    main()
