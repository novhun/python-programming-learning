#!/usr/bin/env python3
"""
Part 06: Advanced OOP & Architecture
-------------------------------------
This runnable script demonstrates:
1. Single inheritance and super()
2. Multiple inheritance, cooperative super(), and Method Resolution Order (MRO)
3. Abstract Base Classes (ABCs) with abc.ABC and @abstractmethod
4. Polymorphism and duck typing
5. Composition over inheritance design
6. Modern Dataclasses (frozen, default_factory, slots)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


# --- 1. Inheritance & super() ---
class Employee:
    def __init__(self, name: str, employee_id: str, base_salary: float) -> None:
        self.name = name
        self.employee_id = employee_id
        self.base_salary = base_salary

    def calculate_pay(self) -> float:
        return self.base_salary

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.name} (ID: {self.employee_id}) - Pay: ${self.calculate_pay():,.2f}"


class Developer(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float, tech_stack: list[str]) -> None:
        super().__init__(name, employee_id, base_salary)
        self.tech_stack = tech_stack

    def calculate_pay(self) -> float:
        # Developers get a 10% tech bonus
        return self.base_salary * 1.10


class Manager(Employee):
    def __init__(self, name: str, employee_id: str, base_salary: float, team_bonus: float) -> None:
        super().__init__(name, employee_id, base_salary)
        self.team_bonus = team_bonus

    def calculate_pay(self) -> float:
        return self.base_salary + self.team_bonus


# --- 2. Multiple Inheritance & MRO (The Diamond Problem) ---
class BaseEntity:
    def describe(self) -> list[str]:
        return ["BaseEntity"]


class AuditableMixin(BaseEntity):
    def describe(self) -> list[str]:
        return ["AuditableMixin"] + super().describe()


class SerializableMixin(BaseEntity):
    def describe(self) -> list[str]:
        return ["SerializableMixin"] + super().describe()


class SecureDocument(AuditableMixin, SerializableMixin):
    def describe(self) -> list[str]:
        return ["SecureDocument"] + super().describe()


# --- 3. Abstract Base Classes (ABCs) & Polymorphism ---
class PaymentGateway(ABC):
    """Abstract contract that all payment gateways must fulfill."""

    @abstractmethod
    def charge(self, amount: float, currency: str) -> bool:
        """Charge the specified amount."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Refund a past transaction."""
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float, currency: str) -> bool:
        print(f"  [Stripe] Charging {amount:.2f} {currency} via Stripe PaymentIntent API.")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"  [Stripe] Refunding txn {transaction_id} through Stripe.")
        return True


class PayPalGateway(PaymentGateway):
    def charge(self, amount: float, currency: str) -> bool:
        print(f"  [PayPal] Charging {amount:.2f} {currency} via PayPal Express Checkout.")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"  [PayPal] Refunding txn {transaction_id} through PayPal.")
        return True


# Polymorphic dispatcher function
def process_customer_checkout(gateway: PaymentGateway, total: float) -> None:
    print(f"Executing checkout with {gateway.__class__.__name__}:")
    success = gateway.charge(total, "USD")
    if success:
        print("  Payment successfully verified!")


# --- 4. Composition Over Inheritance ---
class V8Engine:
    def start(self) -> str:
        return "V8 Engine roaring to life (450 HP)!"


class GPSNavigator:
    def route_to(self, destination: str) -> str:
        return f"Calculating optimal route to {destination}..."


class SportsCar:
    """SportsCar HAS-A Engine and HAS-A GPSNavigator (Composition)."""

    def __init__(self, model: str) -> None:
        self.model = model
        self.engine = V8Engine()  # Composed component
        self.gps = GPSNavigator()  # Composed component

    def drive(self, destination: str) -> None:
        print(f"Starting {self.model}:")
        print(f"  {self.engine.start()}")
        print(f"  {self.gps.route_to(destination)}")


# --- 5. Dataclasses ---
@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    db_name: str
    username: str
    timeout_seconds: int = 30


@dataclass
class ProjectRecord:
    project_id: str
    title: str
    tags: list[str] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2)


def main() -> None:
    print("╔═══════════════════════════════════════════════╗")
    print("║        Part 06: Advanced OOP                  ║")
    print("╚═══════════════════════════════════════════════╝")

    section("1. Inheritance & Method Overriding")
    dev = Developer("Grace Hopper", "E-101", 120000.0, ["Python", "Rust", "Assembly"])
    mgr = Manager("Ada Lovelace", "E-001", 140000.0, 25000.0)

    print(dev)
    print(f"  Tech stack: {', '.join(dev.tech_stack)}")
    print(mgr)

    section("2. Multiple Inheritance & Method Resolution Order (MRO)")
    doc = SecureDocument()
    print("MRO Resolution Chain:")
    print(" -> ".join(cls.__name__ for cls in SecureDocument.mro()))
    print(f"Describe calls traversal: {doc.describe()}")

    section("3. Abstract Contracts & Polymorphism")
    stripe = StripeGateway()
    paypal = PayPalGateway()

    process_customer_checkout(stripe, 149.99)
    process_customer_checkout(paypal, 89.50)

    # Verifying ABC enforcement
    try:
        # Cannot instantiate incomplete abstract class
        PaymentGateway()  # type: ignore
    except TypeError as err:
        print(f"\nCaught expected ABC instantiation error:\n  {err}")

    section("4. Composition Design Pattern")
    car = SportsCar("Apex GT-500")
    car.drive("Silicon Valley Tech Park")

    section("5. Modern Dataclasses")
    db_cfg = DatabaseConfig("db.production.aws.internal", 5432, "analytics_db", "readonly_user")
    print(f"Immutable Dataclass: {db_cfg}")
    print(f"Host: {db_cfg.host}, Port: {db_cfg.port}")

    try:
        db_cfg.port = 3306  # type: ignore
    except Exception as err:
        print(f"Caught mutation error on frozen dataclass: {err.__class__.__name__}")

    proj = ProjectRecord("PROJ-99", "Autonomous Drone Swarm", tags=["robotics", "ai", "python"])
    print(f"\nMutable Dataclass to JSON:\n{proj.to_json()}")

    print("\n✅ Part 06 execution complete!")


if __name__ == "__main__":
    main()
