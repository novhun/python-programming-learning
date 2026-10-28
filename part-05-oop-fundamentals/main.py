#!/usr/bin/env python3
"""
Part 05: OOP Fundamentals
--------------------------
This runnable script demonstrates:
1. Defining classes with __init__ and instance attributes
2. Class attributes vs Instance attributes
3. Instance methods, @classmethod (factories), and @staticmethod (utilities)
4. Encapsulation with private/protected attributes and @property getters/setters
5. Essential Dunder methods: __repr__, __str__, __eq__, __lt__, __add__
"""

from __future__ import annotations


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


class BankAccount:
    """Represents a commercial bank account."""

    # Class attributes (shared across all instances)
    BANK_NAME: str = "Apex Federal Bank"
    INTEREST_RATE: float = 0.035  # 3.5%
    _account_counter: int = 1000

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        # Private/protected instance attributes
        BankAccount._account_counter += 1
        self.account_number = f"ACC-{BankAccount._account_counter}"
        self._owner = owner
        self._balance = 0.0
        self.balance = initial_balance  # Uses the property setter for validation

    # Property Getter
    @property
    def owner(self) -> str:
        return self._owner

    # Property Getter
    @property
    def balance(self) -> float:
        return self._balance

    # Property Setter with validation
    @balance.setter
    def balance(self, amount: float) -> None:
        if amount < 0:
            raise ValueError(f"Balance cannot be negative! Attempted to set: {amount}")
        self._balance = round(float(amount), 2)

    # Instance method
    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"[{self.account_number}] Deposited ${amount:.2f}. New Balance: ${self.balance:.2f}")
        return self.balance

    # Instance method
    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds! Available: ${self.balance:.2f}, Requested: ${amount:.2f}")
        self.balance -= amount
        print(f"[{self.account_number}] Withdrew ${amount:.2f}. New Balance: ${self.balance:.2f}")
        return self.balance

    # Class Method: Factory constructor from formatted string
    @classmethod
    def from_string(cls, record: str) -> BankAccount:
        """Creates an account from a CSV string: 'Owner,InitialBalance'."""
        name, balance_str = record.split(",")
        return cls(owner=name.strip(), initial_balance=float(balance_str.strip()))

    # Static Method: Utility logic independent of instance state
    @staticmethod
    def is_valid_account_number(acc_num: str) -> bool:
        """Validates that account numbers follow format ACC-XXXX."""
        parts = acc_num.split("-")
        return len(parts) == 2 and parts[0] == "ACC" and parts[1].isdigit()

    # Dunder methods
    def __str__(self) -> str:
        """End-user readable representation."""
        return f"{self.BANK_NAME} Account [{self.account_number}] - Owner: {self.owner}, Balance: ${self.balance:.2f}"

    def __repr__(self) -> str:
        """Developer unambiguous representation."""
        return f"BankAccount(owner={self.owner!r}, initial_balance={self.balance})"

    def __eq__(self, other: object) -> bool:
        """Equality based on balance and owner."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance == other.balance and self.owner == other.owner

    def __lt__(self, other: BankAccount) -> bool:
        """Allows sorting accounts by balance."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance

    def __add__(self, other: BankAccount) -> BankAccount:
        """Combine two accounts of the same owner into a consolidated account."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        if self.owner != other.owner:
            raise ValueError("Cannot combine accounts owned by different individuals.")
        consolidated = BankAccount(owner=self.owner, initial_balance=self.balance + other.balance)
        return consolidated


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║        Part 05: OOP Fundamentals              ║")
    print("╚═══════════════════════════════════════════════╝")

    section("1. Instantiation & Methods")
    acc1 = BankAccount("Alice Smith", 500.0)
    print(acc1)
    acc1.deposit(250.0)
    acc1.withdraw(120.0)

    section("2. Property Setter & Validation")
    try:
        print("Attempting to set negative balance (-50)...")
        acc1.balance = -50.0
    except ValueError as err:
        print(f"Caught expected validation error: {err}")

    section("3. Class Methods (Factory) & Static Methods")
    acc2 = BankAccount.from_string("Bob Johnson, 1500.0")
    print(f"Created via @classmethod from_string:\n  {acc2}")

    print("\nStatic method validation:")
    print(f"  Is 'ACC-1002' valid? {BankAccount.is_valid_account_number('ACC-1002')}")
    print(f"  Is 'XYZ-9999' valid? {BankAccount.is_valid_account_number('XYZ-9999')}")

    section("4. Magic / Dunder Methods (__repr__, __add__, __lt__)")
    print(f"repr(acc1): {repr(acc1)}")
    print(f"repr(acc2): {repr(acc2)}")

    # Account consolidation with __add__
    alice_savings = BankAccount("Alice Smith", 2000.0)
    merged_alice = acc1 + alice_savings
    print(f"\nMerged Account (acc1 + alice_savings):\n  {merged_alice}")

    # Sorting accounts with __lt__
    accounts = [acc2, acc1, alice_savings]
    print("\nAccounts before sort:")
    for a in accounts:
        print(f"  {a.owner:<15} : ${a.balance:,.2f}")

    accounts.sort()
    print("\nAccounts sorted by balance (ascending via __lt__):")
    for a in accounts:
        print(f"  {a.owner:<15} : ${a.balance:,.2f}")

    print("\n✅ Part 05 execution complete!")


if __name__ == "__main__":
    main()
