export class Employee {
  emp_name?: string;
  emp_id?: string;
  org_id?: string;
  date_of_joining?: string;
  emp_role?: string;
  emp_location?: string;
  employees_count?: number
}

export class Organization {
  name?: string;
  org_id?: string;
  location?: string;
  employees_count?: number
}

export type MultiSelect = {
  role: string;
  location: string;
}

export type FilterStructure = {
  [key: string]: Employee[];
}

export type FilterSelection = {
  groupLabel: string;
  value: string;
}