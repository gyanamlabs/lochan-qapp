"""The starter package declares on its PackageBase subclass (Q-S3-KTG6 D1)."""
import asyncio

from aadhaar import package_declaration, resolve_packagebase_instance

from demo import package


def test_the_module_resolves_to_demo_package():
    pkg = resolve_packagebase_instance(package)
    assert (type(pkg).__name__, pkg.name, pkg.prefix) == ("DemoPackage", "demo", "demo")


def test_rbac_is_declared_on_the_class():
    """trishul seeds these from the class; a module-level binding is refused."""
    assert [(r[0], r[3]) for r in package_declaration(package, "PACKAGE_ROLES")] == [
        ("demo.admin", True), ("demo.user", False),
    ]
    assert package_declaration(package, "ROLE_PERMISSIONS")["demo.user"] == ["demo.view"]


def test_health_is_the_framework_default():
    result = asyncio.run(resolve_packagebase_instance(package).health_check())
    assert (result["status"], result["package"]) == ("healthy", "demo")
