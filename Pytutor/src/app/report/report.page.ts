import { Component } from '@angular/core';
import { ReportService } from '../services/report.service'

@Component({
  selector: 'app-report',
  templateUrl: 'report.page.html',
  styleUrls: ['report.page.scss']
})
export class ReportPage {
  constructor(public ReportService: ReportService) {}

  loadReportPage() {
    this.ReportService.loadReport();
  }
}
