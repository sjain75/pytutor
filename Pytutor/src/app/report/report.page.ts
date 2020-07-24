import { Component } from '@angular/core';
import { ReportService } from '../services/report.service'

@Component({
  selector: 'app-report',
  templateUrl: 'report.page.html',
  styleUrls: ['report.page.scss']
})
export class ReportPage {
  constructor(private ReportService: ReportService) {}

  public loadReportPage() {
    this.ReportService.loadReport();
  }
}
