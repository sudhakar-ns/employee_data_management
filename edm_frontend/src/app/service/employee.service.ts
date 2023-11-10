import { Injectable } from '@angular/core';
import { Observable, map, of } from 'rxjs';
import { Employee, Organization } from '../models/employee';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {

  constructor(private http: HttpClient) { }

  public loadEmployeeDetails(): Observable<Employee[]> {
    return this.http.get('http://127.0.0.1:5000/get_employee_data').pipe(
      map((res: any) => res.message)
    );
  }

  public loadOrgDetails(): Observable<Organization> {
    return this.http.get('http://127.0.0.1:5000/get_org_data').pipe(
      map((res: any) => res.message[0])
    );
  }

  public addEmployeeDetail(employee: Employee) {
    return this.http.post('http://127.0.0.1:5000/add_employee', employee).pipe(
      map((res: any) => res)
    );
  }

  public updateEmployeeDetail(employee: Employee) {
    return this.http.post('http://127.0.0.1:5000/update_employee', employee).pipe(
      map((res: any) => res)
    );
  }

  public deleteEmployeeDetail(employee: Employee) {
    return this.http.post('http://127.0.0.1:5000/remove_employee', employee).pipe(
      map((res: any) => res)
    );
  }
}
