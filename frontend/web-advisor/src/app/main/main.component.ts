import { Component, OnInit } from '@angular/core';
import { ServiceMain } from '../service.main';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  description = 'Советник готов советовать!';

  fileType = "";
  selectedFile: File | null = null;
  isLoading: boolean = false;

  activity: string = ''; 
  category: string = '';

  activitysOptions: string[] = ['frontend', 'devops', 'backend'];
  categoryOptions: string[] = ['Resume', 'Vacancy'];


  constructor(private service: ServiceMain, private router: Router) { }
  ngOnInit(): void {localStorage.clear();}



  setFileType(type: string) {
    this.fileType = type;
    console.log("Выбран тип файла: " + this.fileType);
  }

  isActive(type: string): boolean {
    return this.fileType === type;
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
    }
  }


  UploadFile() {
    if (!this.selectedFile) {
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);
    formData.append('category', this.category);
    formData.append('activity', this.activity);
    
    this.isLoading = true;

    this.service.handle_post_requests(formData, 'advice/generate').subscribe(response => {
      console.log('Ответ от сервера:', response);
      localStorage.setItem('rank', JSON.stringify(response.response));

      this.isLoading = false;
      this.router.navigate(['rank']);
    },
      error => {
        if (error.status === 400) {
          console.error('Ошибка от сервера:', error.error.detail);
          alert('Ошибка: ' + error.error.detail); 
        }
        this.isLoading = false;
      }
    );
  }
}
