import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-rank',
  templateUrl: './rank.component.html',
  styleUrls: ['./rank.component.scss']
})
export class RankComponent implements OnInit {
  items: { title: string, value: string }[] = [];
  isDialogOpen = false;
  dialogContent = '';

  constructor(private location: Location, private route: ActivatedRoute, private router: Router) { }
  ngOnInit(): void {
    this.getData();
  }
  

  getData(): void {
    try {
      const rankData = localStorage.getItem('rank');
      if (!rankData) {
        this.router.navigate(['main']);
        return;
      }
      if (rankData) {
        const parsedData = JSON.parse(rankData);
        console.log(parsedData);
        if (Array.isArray(parsedData)) {
          this.items = parsedData;
        } else {
          console.error('Данные rank не являются массивом');
        }
      }
    } catch (error) {
      console.error('Ошибка парсинга rank данных:', error);
    }
  }

  goBack(): void {
    this.location.back();
  }


  openDialog(content: string): void {
    this.dialogContent = content;
    this.isDialogOpen = true;
  }

  closeDialog(): void {
    this.isDialogOpen = false;
    this.dialogContent = '';
  }
}
