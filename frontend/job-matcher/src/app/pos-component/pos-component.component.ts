import { Component, Input } from '@angular/core';
import { DISPLAY_POS, POSData} from '../models/pos';
import { NgFor, NgIf, SlicePipe } from '@angular/common';
import { Token } from '../models/token';

@Component({
  selector: 'app-pos-component',
  standalone: true,
  imports: [
    NgFor,
    NgIf,
    SlicePipe,
  ],
  templateUrl: './pos-component.component.html',
  styleUrl: './pos-component.component.scss'
})
export class PosComponentComponent {
  @Input() data?: POSData;
  @Input() type?: string;
  maxDisplayed = 10;
  showAll = false;

  isDisplayType(): boolean {
    const type = this.type;
    if (!type) {
      return false
    }
    return DISPLAY_POS.includes(type)
  }

  toggleShowAll() {
    const type = this.type;
    const data = this.data;
    if (!type || !data){
      return
    }
    if (this.maxDisplayed > 10){
      this.maxDisplayed = 10;
      this.showAll = false;
    } else {
      this.maxDisplayed = data[type].length;
      this.showAll = true;
    }
  }

  getWords() : Token[] {
    const type = this.type;
    const data = this.data;
    if (!type || !data){
      return []
    }
    return data[type];
  }

  min(a:number, b:number): number {
    return Math.min(a, b);
  }
}
