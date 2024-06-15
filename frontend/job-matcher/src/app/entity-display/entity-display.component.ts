import { Component, Input } from '@angular/core';
import { Entity } from '../models/entity';
import { NgFor, NgIf, SlicePipe } from '@angular/common';

@Component({
  selector: 'app-entity-display',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    SlicePipe,
  ],
  templateUrl: './entity-display.component.html',
  styleUrl: './entity-display.component.scss'
})
export class EntityDisplayComponent {
  @Input() entities?: Entity[];
  
  maxDisplayed = 10;
  showAll = false;

  toggleShowAll() {
    const entities = this.entities;
    if(!entities){
      return;
    }
    if (this.maxDisplayed > 10){
      this.maxDisplayed = 10;
      this.showAll = false;
    } else {
      this.maxDisplayed = entities.length;
      this.showAll = true;
    }
  }

  min(a:number, b:number): number {
    return Math.min(a, b);
  }
}
