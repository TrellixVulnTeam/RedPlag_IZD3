import { Component, OnInit } from '@angular/core';
import { GraphServiceService } from '../graph-service.service';


@Component({
  selector: 'app-visualization',
  templateUrl: './visualization.component.html',
  styleUrls: ['./visualization.component.css']
})
export class VisualizationComponent implements OnInit {
	blob: Blob;
	imageToShow; 
  constructor(private gs: GraphServiceService) { }

  ngOnInit(): void {
  }
  // createImageFromBlob(image: Blob) {
  //    let reader = new FileReader();
  //    reader.addEventListener("load", () => {
  //       this.imageToShow = reader.result; <<< this.imageToShow
  //    }, false);
  
  //    if (image) {
  //       reader.readAsDataURL(image);
  //       console.log(image);
  //    }
  // }
    
  get_image():void{
    this.gs.getHistogram().subscribe(data=>{
      // this.createImageFromBlob(data);
    this.blob = new Blob([data as BlobPart], {type: 'image/png'});
    // this.createImageFromBlob(this.blob);
    console.log("hello");
    console.log(data);
  })}

}
