from analyser import Analyser

def test_get_all_ancestors():
    ast = {
        "roles": [
            {"name": "Admin", "parents": ["SuperUser"], "permissions": []},
            {"name": "SuperUser", "parents": ["User"], "permissions": []},
            {"name": "User", "parents": ["Guest"], "permissions": []},
            {"name": "Guest", "parents": [], "permissions": []},
            {"name": "Manager", "parents": ["User", "Editor"], "permissions": []},
            {"name": "Editor", "parents": ["User"], "permissions": []}
        ],
        "conflicts": []
    }
    
    analyser = Analyser(ast)
    analyser._build_roles()
    
    # Test simple inheritance
    assert analyser.get_all_ancestors("Admin") == {"SuperUser", "User", "Guest"}
    print("Test Admin passed")
    
    # Manager -> User, Editor
    # User -> Guest
    # Editor -> User -> Guest
    expected_manager = {"User", "Editor", "Guest"}
    actual_manager = analyser.get_all_ancestors("Manager")
    assert actual_manager == expected_manager, f"Expected {expected_manager}, got {actual_manager}"
    print("Test Manager passed")
    
    # Test no parents
    assert analyser.get_all_ancestors("Guest") == set()
    print("Test Guest passed")
    
    # Test undefined role
    assert analyser.get_all_ancestors("NonExistent") == set()
    print("Test NonExistent passed")

    print("All get_all_ancestors tests passed!")

if __name__ == "__main__":
    test_get_all_ancestors()
