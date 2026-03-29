import copy

class Optimizer:
    def __init__(self, ast):
        self.ast = copy.deepcopy(ast)
        self.roles_dict = {r["name"]: r for r in self.ast["roles"]}

    def get_all_ancestors(self, role_name):
        ancestors = set()
        data = self.roles_dict.get(role_name)
        if not data:
            return ancestors
            
        for parent in data.get("parents", []):
            ancestors.add(parent)
            ancestors.update(self.get_all_ancestors(parent)) 
       
        return ancestors
        
    def get_inherited_permissions(self, role_name):
        perms = set()
        for ancestor in self.get_all_ancestors(role_name):
            anc_data = self.roles_dict.get(ancestor)
            if anc_data:
                perms.update(anc_data.get("permissions", []))
      
        return perms
            
    def optimize(self):
        
        for role in self.ast["roles"]:
            role["parents"] = list(dict.fromkeys(role["parents"]))
            role["permissions"] = list(dict.fromkeys(role["permissions"]))

        
        for role in self.ast["roles"]:
            direct_parents = role["parents"]
            redundant_parents = set()

            for p1 in direct_parents:
                for p2 in direct_parents:
                    if p1 == p2:
                        continue
                    if p1 in self.get_all_ancestors(p2):
                        redundant_parents.add(p1)

            role["parents"] = [p for p in direct_parents if p not in redundant_parents]

        
        for role in self.ast["roles"]:
            inherited_perms = self.get_inherited_permissions(role["name"])
            explicit_perms = role["permissions"]
            role["permissions"] = [p for p in explicit_perms if p not in inherited_perms]

       
        seen_conflicts = set()
        optimized_conflicts = []
        
        # FIX: Corrected quote placement in "conflicts", []
        for r1, r2 in self.ast.get("conflicts", []):
            pair = tuple(sorted([r1, r2]))
            if pair not in seen_conflicts:
                seen_conflicts.add(pair)
               
                optimized_conflicts.append((r1, r2))
                
       
        self.ast["conflicts"] = optimized_conflicts
        return self.ast