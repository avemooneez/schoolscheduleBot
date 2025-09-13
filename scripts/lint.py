#!/usr/bin/env python3
"""
Скрипт для запуска всех линтеров и проверок кода.
Использование: poetry run python scripts/lint.py [--fix]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Запускает команду и возвращает True если успешно."""
    print(f"\n🔍 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Запуск линтеров и проверок кода")
    parser.add_argument(
        "--fix", action="store_true", help="Автоматически исправлять ошибки"
    )
    parser.add_argument(
        "--ruff-only", action="store_true", help="Запустить только Ruff"
    )
    parser.add_argument(
        "--black-only", action="store_true", help="Запустить только Black"
    )
    parser.add_argument(
        "--mypy-only", action="store_true", help="Запустить только mypy"
    )
    args = parser.parse_args()

    # Определяем команды в зависимости от флагов
    commands = []

    if args.ruff_only:
        commands = [
            (
                "ruff",
                ["ruff", "check", ".", "--fix"] if args.fix else ["ruff", "check", "."],
            )
        ]
    elif args.black_only:
        commands = [("black", ["black", "."])]
    elif args.mypy_only:
        commands = [("mypy", ["mypy", "."])]
    else:
        # Все проверки
        commands = [
            (
                "ruff check",
                ["ruff", "check", ".", "--fix"] if args.fix else ["ruff", "check", "."],
            ),
            (
                "ruff format",
                (
                    ["ruff", "format", "."]
                    if args.fix
                    else ["ruff", "format", "--check", "."]
                ),
            ),
            ("black", ["black", "."] if args.fix else ["black", "--check", "."]),
            ("isort", ["isort", "."] if args.fix else ["isort", "--check-only", "."]),
            ("mypy", ["mypy", "."]),
        ]

    # Запускаем команды
    success = True
    for description, cmd in commands:
        if not run_command(cmd, description):
            success = False

    if success:
        print("\n🎉 Все проверки прошли успешно!")
        sys.exit(0)
    else:
        print("\n💥 Некоторые проверки не прошли. Исправьте ошибки и попробуйте снова.")
        if not args.fix:
            print(
                "💡 Попробуйте запустить с флагом --fix для автоматического исправления:"
            )
            print("   poetry run python scripts/lint.py --fix")
        sys.exit(1)


if __name__ == "__main__":
    main()
