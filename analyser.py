class Analyser:
    def __init__(self, ast):
        self.ast = ast
        self.roles = {}
        self.errors = []
        self.resolved_cache = {}

    def _build_roles(self):
        for r in self.ast.get("roles", []):
            name = r["name"]
            if name in self.roles:
                self.errors.append(
                    f"[SEMANTIC] Duplicate role definition: '{name}' is defined more than once."
                )
                continue
            self.roles[name] = r
            
    def check_empty_policy(self):
        if not self.ast.get("roles"):
            self.errors.append("[SEMANTIC] Empty policy: at least one role must be defined.")

    def check_undefined_parents(self):
        for role_name, data in self.roles.items():
            for parent in data.get("parents", []):
                if parent not in self.roles:
                    self.errors.append(
                        f"[SEMANTIC] Unidentified parent: role '{role_name}' inherits from undefined role '{parent}'."
                    )

    def check_conflict_references(self):
        for r1, r2 in self.ast.get("conflicts", []):
            if r1 not in self.roles:
                self.errors.append(f"[SEMANTIC] Undefined role in conflict: '{r1}' is not a defined role.")
            if r2 not in self.roles:
                self.errors.append(f"[SEMANTIC] Undefined role in conflict: '{r2}' is not a defined role.")

    def check_self_conflict(self):
        """Check if a conflict with itself is present"""
        for r1, r2 in self.ast.get("conflicts", []):
            if r1 == r2:
                self.errors.append(f"[SEMANTIC] self-conflict invalid: conflict '{r1}','{r2}' references the same role.")

    def check_duplicate_conflict(self):
        """Same conflict pair or reversed should not appear twice """
        seen = set()
        for r1, r2 in self.ast["conflicts"]:
            pair = (min(r1,r2),max(r1,r2))
            if pair in seen:
                self.errors.append(f"[SEMANTIC] Duplicate conflict: conflict '{r1}','{r2}' are repeated.")
            seen.add(pair)

    def check_cycles(self):
        """ Standard DFS to detect cycles in the inheritance graph"""
        if not self.roles or self.errors:
            return
            
        visited = set()
        stack = set()

        def visit(node):
            visited.add(node)
            stack.add(node)
            
            for parent in self.roles.get(node, {}).get("parents", []):
                
                if parent not in self.roles:
                    continue 
                
                if parent not in visited:
                    if visit(parent):
                        return True
                elif parent in stack:
                    return True
            
            stack.remove(node)
            return False

        for role in self.roles:
            if role not in visited:
                if visit(role):
                    self.errors.append(
                        f"[CRITICAL] Cycle detected in inheritance chain involving '{role}'."
                    )

    def get_all_ancestors(self, role_name):
        """Returns a set of all roles inherited by this role"""
        ancestors = set()
        data = self.roles.get(role_name)
        if not data:
            return ancestors
        for parent in data.get("parents", []):
            if parent in self.roles:
                ancestors.add(parent)
                ancestors.update(self.get_all_ancestors(parent))
        return ancestors

    def check_sod(self):
        """Check Seperation of Duty: no role may inherit both sides of a conflict"""
        if not self.roles or self.errors:
            return
        for r1,r2 in self.ast["conflicts"]:
            if r1 not in self.roles or r2 not in self.roles:
                continue
            for role_name in self.roles:
                ancestors = self.get_all_ancestors(role_name)
                has_r1 = (role_name==r1) or (r1 in ancestors)
                has_r2 = (role_name==r2) or (r2 in ancestors)

                if has_r1 and has_r2:
                    self.errors.append(
                        f"[SECURITY] SoD Violation:Role '{role_name}' inherits conflicting roles '{r1}' and '{r2}'."
                    )
    
    def run(self):
        self._build_roles()
        self.check_empty_policy()
        self.check_undefined_parents()
        self.check_conflict_references()
        self.check_self_conflict()
        self.check_duplicate_conflict()
        self.check_cycles()
        
        if not self.errors:
            self.check_sod()
        return self.errors
    

    #End