import { Component, OnInit } from '@angular/core';
import { FactorService } from '../shared/factor/factor.service';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-factor-list',
  templateUrl: './factor-list.component.html',
  styleUrls: ['./factor-list.component.css']
})

export class FactorListComponent implements OnInit {
  factors: Array<any>;
  top_result: any;
  old_results: Array<any>;
  intervalHolder: any;

  constructor(private factorService: FactorService) { }

  update_factor(factor) {
    if (factor.result_msg == null) {
      console.log('got factor with null msg');
      return;
    }

    var started = new Date(factor.request_ts);
    var now = new Date(factor.now_ts);
    if (factor.result_msg == "pending") {
      var diff_ms = now.getTime() - started.getTime();
      var elapsed_sec = (diff_ms / 1000).toFixed(3)
      factor.status = "pending for " + elapsed_sec + " seconds";
    } else {
      var finished = new Date(factor.result_ts);
      var diff_ms = finished.getTime() - started.getTime();
      var diff_sec = (diff_ms / 1000).toFixed(3)
      factor.status = factor.result_msg + " in " + diff_sec + " seconds"
    }
    if (factor.result_list.length == 1) {
      factor.status = factor.status + ' as prime!';
    }

    factor.prod_list = [];
    factor.result_list.sort(function (a, b) { return a - b });
    factor.result_list.forEach((result) => {
      var c = factor.number / result;
      factor.prod_list.push(result + ' \u00D7 ' + c.toFixed());
    });
  }

  update_view() {
    var new_factors = [];
    this.old_results.forEach((result) => {
      if (this.top_result != null &&
        this.top_result.number == result.number) {
        // put the top result at the beginning of the array
        result.top = true;
        new_factors.unshift(result);
      } else {
        result.top = false;
        new_factors.push(result);
      }
    });
    if (this.top_result != null &&
      new_factors.length > 0 &&
      this.top_result.number != new_factors[0].number) {
      this.top_result.top = true;
      new_factors.unshift(this.top_result);
    }
    new_factors.forEach((factor) => {
      this.update_factor(factor);
    })
    this.factors = new_factors;
  }

  update_from_server_all() {
    this.factorService.getAll().subscribe(results => {
      console.log('refreshing factors');
      this.old_results = results;
      this.update_view();
    });
  }

  update_from_server_one(number) {
    this.factorService.get(number).subscribe(result => {
      this.top_result = result;
      this.update_view();
    }, error => console.error(error));
  }

  ngOnInit(): void {
    this.update_from_server_all();

    this.intervalHolder = setInterval(() => {
      var num_pending_factors = 0;
      this.factors.forEach((factor) => {
        if (factor.result_msg == "pending") {
          num_pending_factors++;
        }
      });
      if (num_pending_factors > 0) {
        console.log(num_pending_factors + " pending tasks, refreshing");
        this.update_from_server_all();
        if (this.top_result != null) {
          this.update_from_server_one(this.top_result.number)
        }
      }
    }, 1000);
  }

  ngOnDestroy(): void {
    clearInterval(this.intervalHolder);
  }

  factor(form: NgForm) {
    var number = form['number'];
    console.log("user entered [" + number + "]");
    if (number == null || number == '') {
      this.top_result = null;
      this.update_view();
    } else {
      this.update_from_server_one(number);
    }
  }
}