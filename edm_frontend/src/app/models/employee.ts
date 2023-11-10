export class Employee {
  emp_name?: string;
  emp_id?: number;
  org_id?: number;
  date_of_joining?: string;
  emp_role?: string;
  emp_location?: string;
  employees_count?: number
}

export class Organization {
  name?: string;
  org_id?: number;
  location?: string;
  employees_count?: number
}
