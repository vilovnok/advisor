import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-rank',
  templateUrl: './rank.component.html',
  styleUrls: ['./rank.component.scss']
})
export class RankComponent implements OnInit {
  items: { title: string, value: string }[] = [];
  
  constructor(private location: Location) {}

  ngOnInit(): void {
    // const rankData = localStorage.getItem('rank');    
    this.items = localStorage.getItem('rank');
    console.log(this.items);
  }

  goBack(): void {
    this.location.back();
  }
}
