import sys
from collections import defaultdict

class CommitOwners:
    def __init__(self):
        self.employees = {}  # id (surname, name)
        
    def load_employees(self, filename):
        # Load employee data from a file
        try:
            with open(filename, 'r', encoding='utf-8') as f: # open the file in read mode
                for line in f: 
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            emp_id = parts[0].strip() # employee ID
                            surname = parts[1].strip() # employee surname
                            name = parts[2].strip() # employee name
                            self.employees[emp_id] = (surname, name) # store in dictionary
            print(f"Loaded {len(self.employees)} employees")
        except Exception as e:
            print(f"Error loading employees: {e}")
            sys.exit(1)
    
    def find_all_decompositions(self, weld, start_pos=0, current_decomp=None):
        """Find all possible ways to decompose the weld string into employee IDs"""
        if current_decomp is None:
            current_decomp = []
        
        # base case, reached end of string
        if start_pos == len(weld): 
            return [current_decomp.copy()] # return a copy of the current decomposition
        
        all_decompositions = []
        
        # try all possible employee IDs starting from current position
        for emp_id in self.employees: 
            if weld[start_pos:].startswith(emp_id): # check if the weld starts with this employee ID
                # this employee ID matches, add to current decomposition
                current_decomp.append(emp_id) 
                
                # recursively find decompositions for the rest
                sub_decomps = self.find_all_decompositions(
                    weld, start_pos + len(emp_id), current_decomp
                )
                all_decompositions.extend(sub_decomps)
                
                # remove last added employee id to try the next possible id
                current_decomp.pop() 
        
        return all_decompositions
    
    def find_best_decomposition(self, weld):
        #find the longest sequence of commits
        all_decomps = self.find_all_decompositions(weld)
        
        if not all_decomps:
            print("No valid decomposition found!")
            return []
        
        print(f"Found {len(all_decomps)} possible decomposition(s)")
        
        # find the decomposition with maximum number of commits
        best_decomp = max(all_decomps, key=len)
        
        print(f"Best decomposition has {len(best_decomp)} commits")
        
        return best_decomp
    
    def solve(self, employees_file, weld):

        print(f"Employees file: {employees_file}")
        print(f"Weld string: {weld}")
        print()
        
        # load employee data
        self.load_employees(employees_file)
        
        if not self.employees:
            print("No employees loaded!")
            return
        
        print(f"Available employee IDs: {sorted(self.employees.keys())}")
        print()
        
        # find best decomposition
        best_sequence = self.find_best_decomposition(weld)
        
        if best_sequence:
            print("\n Longest Commit sequence (one per line):")
            for emp_id in best_sequence:
                surname, name = self.employees[emp_id]
                print(f"{emp_id}: {surname}, {name}")
        else:
            print("No valid sequence found!")

def main():
    if len(sys.argv) != 3: # check if the correct number of arguments is provided
        print("Example: python commit_owners.py employees.txt 123456")
        sys.exit(1)
    
    employees_file = sys.argv[1]
    weld = sys.argv[2]
    
    solver = CommitOwners()
    solver.solve(employees_file, weld)

if __name__ == "__main__":
    main()