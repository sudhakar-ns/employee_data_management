import { Component, ElementRef, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

import { DatePipe } from '@angular/common';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatSort } from '@angular/material/sort';
import { Employee, Organization } from '../models/employee';
import { EmployeeService } from '../service/employee.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})

export class MainComponent implements OnInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild('addEditDialogTemplate') addEditDialogTemplate!: TemplateRef<any>;
  @ViewChild('deleteDialogTemplate') deleteDialogTemplate!: TemplateRef<any>;
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;
  @ViewChild(MatSort) sort!: MatSort;

  public EmployeeFormGroup: FormGroup;
  public currentMode = 'View';
  public employeeEntity!: Employee;
  public dataSource!: MatTableDataSource<Employee>;
  public empDataDisplayedColumns: string[] = ['emp_name', 'emp_id', 'date_of_joining', 'emp_role', 'emp_location', 'actions'];
  public canExpandOrgSection = false;
  public orgData!: Organization;
  selectedFile: File | null = null;

  constructor(public dialog: MatDialog, private employeeService: EmployeeService, private datePipe: DatePipe, private snackbar: MatSnackBar) {
    this.EmployeeFormGroup = new FormGroup({
      emp_id: new FormControl('', [Validators.required, this.duplicateIDValidator()]),
      emp_name: new FormControl('', [Validators.required]),
      date_of_joining: new FormControl('', [Validators.required]),
      emp_role: new FormControl('', [Validators.required]),
      emp_location: new FormControl('', [Validators.required])
    });
  }

  ngOnInit(): void {
    this.employeeService.loadEmployeeDetails().subscribe((data) => {
      this.dataSource = new MatTableDataSource<Employee>(data);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    });
    this.employeeService.loadOrgDetails().subscribe((data) => {
      this.orgData = data;
    });
  }

  expandOrgDet(): void {
    this.canExpandOrgSection = !this.canExpandOrgSection;
  }

  deleteRow(employee: Employee): void {
    this.employeeEntity = employee;
    this.employeeEntity.org_id = this.orgData.org_id;
    this.employeeEntity.employees_count = this.orgData.employees_count;
    const dialogRef = this.dialog.open(this.deleteDialogTemplate, { width: '400px' });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.employeeService.deleteEmployeeDetail(this.employeeEntity).subscribe({
          next: () => {
            const ind = this.dataSource.data.findIndex(({ emp_id }) => emp_id === this.employeeEntity.emp_id);
            let clonedData = this.dataSource.data;
            if (ind !== -1) clonedData.splice(ind, 1);
            this.dataSource.data = clonedData;
            if (this.orgData?.employees_count) this.orgData.employees_count--;
            this.showToast('Employee record deleted successfully', 'success-toast');
          },
          error: (err) => {
            this.showToast(err.message, 'failure-toast');
          }
        });
      }
    });
  }

  onSubmit(): void {
    if (this.currentMode.toLowerCase() === 'add') this.employeeEntity = new Employee();
    if (this.EmployeeFormGroup.valid) {
      // Handle the form submission here
      this.employeeEntity.org_id = this.orgData.org_id;
      this.employeeEntity.employees_count = this.orgData.employees_count;
      this.employeeEntity.emp_id = this.EmployeeFormGroup.value.emp_id;
      this.employeeEntity.emp_name = this.EmployeeFormGroup.value.emp_name;
      this.employeeEntity.date_of_joining = this.datePipe.transform(this.EmployeeFormGroup.value.date_of_joining, 'dd-MM-YYYY') ?? new Date().getDate().toString();
      this.employeeEntity.emp_role = this.EmployeeFormGroup.value.emp_role;
      this.employeeEntity.emp_location = this.EmployeeFormGroup.value.emp_location;
      if (this.currentMode.toLowerCase() === 'add') {
        this.employeeService.addEmployeeDetail(this.employeeEntity).subscribe({
          next: () => {
            const updatedData = [this.employeeEntity, ...this.dataSource.data];
            this.dataSource.data = updatedData;
            if (this.orgData?.employees_count) this.orgData.employees_count++;
            this.showToast('Employee added successfully', 'success-toast');
          },
          error: (err) => {
            this.showToast(err.message, 'failure-toast');
          }
        });
      } else {
        this.employeeService.updateEmployeeDetail(this.employeeEntity).subscribe({
          next: () => {
            const updatedEntity = this.dataSource.data.find(({ emp_id }) => emp_id === this.employeeEntity.emp_id);
            const ind = this.dataSource.data.findIndex(({ emp_id }) => emp_id === this.employeeEntity.emp_id);
            const clonedDataSource = this.dataSource.data;
            if (ind !== -1) {
              clonedDataSource[ind] = { ...clonedDataSource[ind], ...updatedEntity }
            }
            this.dataSource.data = clonedDataSource;
            this.showToast('Employee updated successfully', 'success-toast');
          },
          error: (err) => {
            this.showToast(err.message, 'failure-toast');
          }
        });
      }
    }
  }

  applyFilter(event: any) {
    const searchedString = event?.target?.value;
    this.dataSource.filter = searchedString?.trim().toLowerCase();
  }

  downloadData(): void {
    this.employeeService.downloadEmployeeDetail().subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'export.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      },
      error: (err) => console.log({ err })
    });
  }

  isValidFileType(file: File): boolean {
    const validTypes = [
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ];
    return validTypes.includes(file.type);
  }

  uploadData(event: any): void {
    console.log({ event });
    this.selectedFile = event.target.files[0];
    if (this.selectedFile) {
      if (this.isValidFileType(this.selectedFile)) {
        const formData = new FormData();
        formData.append('file', this.selectedFile, this.selectedFile.name);

        this.employeeService.uploadEmployeeDetail(formData).subscribe({
          next: () => {
            this.showToast("Invalid file type.", 'failure-toast');
          },
          error: (err) => this.showToast(err.error.message, 'failure-toast')
        });
      } else {
        this.showToast("Invalid file type.", 'failure-toast');
        // Handle the invalid file type here
      }
      this.fileInput.nativeElement.value = '';
    }
  }

  openDialog(title: string, employee?: Employee): void {
    this.currentMode = title;

    if (title === 'Add') {
      this.EmployeeFormGroup.reset();
    } else {
      if (employee) {
        this.employeeEntity = employee;
        this.updateForm(this.employeeEntity)
      }
    }
    this.dialog.open(this.addEditDialogTemplate, {
      width: '400px',
      data: { title, ...employee }, // Pass the title and data to the dialog
    });
  }

  private updateForm(employeeEntity: Employee) {
    this.EmployeeFormGroup.patchValue({
      emp_name: employeeEntity.emp_name,
      emp_id: employeeEntity.emp_id,
      date_of_joining: employeeEntity.date_of_joining ? new Date(employeeEntity.date_of_joining) : new Date().getDate().toString(),
      emp_location: employeeEntity.emp_location,
      emp_role: employeeEntity.emp_role
    });
  }

  private showToast(message: string, toastType: string): void {
    this.snackbar.open(message, 'Close', {
      duration: 3000,
      panelClass: toastType
    })
  }

  private duplicateIDValidator() {
    return (control: any) => {
      const value = control?.value;
      const isDuplicate = this.dataSource?.data?.some(({ emp_id }) => emp_id === value);

      return isDuplicate && this.currentMode.toLowerCase() === 'add' ? { duplicateId: true } : null;
    }
  }

}
