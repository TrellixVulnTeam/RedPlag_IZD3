import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FileService } from '../file.service';
import { Router, ActivatedRoute } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { AlertService } from '../alert.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
	selector: 'app-red-plag',
	templateUrl: './red-plag.component.html',
	styleUrls: ['./red-plag.component.scss']
})


export class RedPlagComponent implements OnInit {
	blob: Blob;
	heatMap: any;
	histogram: any;
	progress = 0;
	selectedFiles: FileList;
	currentFile: File;
	blob2: Blob;
 	message;
	formGroup : FormGroup;

	constructor(private fb: FormBuilder, private fileService: FileService, private router: Router, private alertService: AlertService, private cd: ChangeDetectorRef,  private sanitizer: DomSanitizer) { }

	ngOnInit(): void {
  		console.log("Red Plag Module initiated");
		this.formGroup = this.fb.group({ file : [''] , boilerplate : [''] , filetype : [''] });
	}
  

	onFileChange(event) {
  		console.log("file changed");
  		let reader = new FileReader();
	
  		if(event.target.files && event.target.files.length) {
    			const uploaded = event.target.files[0];
			console.log(uploaded);
    			this.formGroup.get('file').setValue(uploaded);
  		}
	}


  	onBoilerPlateChange(event) {
    		console.log("boilerplate changed");
    		let reader = new FileReader();
	
    		if(event.target.files && event.target.files.length) {
    			const boilerPlate = event.target.files[0];
    			console.log(boilerPlate);
     			this.formGroup.get('boilerplate').setValue(boilerPlate);
    		}
  	}


	onRadioChange(event){
		console.log("file type changed");
		const fileType = event.target.value;
		this.formGroup.get('filetype').setValue(fileType);
	}

	onSubmit() {
  		console.log("file upload ts");
  		console.log(this.formGroup.value.file);
  		console.log(this.formGroup.value.boilerplate);
  		console.log(this.formGroup.value.filetype);
  		this.fileService.postFile(this.formGroup.value.file, this.formGroup.value.boilerplate, this.formGroup.value.filetype).subscribe( 
			event => {console.log(event);},
    			err => {
    				this.progress = 0;
      				this.message = 'Could not upload the file!';
    		});
	}

	onProcessFiles() {
		this.fileService.processFiles().subscribe((data) => {});
	}

	onDownloadButtonClick() {
    		console.log("download ts");
    		this.fileService.getProcessedFiles().subscribe((data) => {
			this.blob = new Blob([data as BlobPart], {type: 'application/zip'});
			var downloadURL = window.URL.createObjectURL(data);
      			var link = document.createElement('a');
      			link.href = downloadURL;
      			link.download = "a.zip";
      			link.click();
    		});
 	}

	onShowResults() {
		console.log("heatmap ts");
		this.fileService.getHeatMap().subscribe((data) => {
			this.blob = new Blob([data as BlobPart], {type: 'image/png'});
			var heatmapURL = window.URL.createObjectURL(data);
			this.heatMap = this.sanitizer.bypassSecurityTrustUrl(heatmapURL);
		});

		this.fileService.getHistogram().subscribe((data) => {
			this.blob = new Blob([data as BlobPart], {type: 'image/png'});
			var histogramURL = window.URL.createObjectURL(data);
			this.histogram = this.sanitizer.bypassSecurityTrustUrl(histogramURL);
		});
	}
}
