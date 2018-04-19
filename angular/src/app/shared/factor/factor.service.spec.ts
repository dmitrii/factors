import { TestBed, inject } from '@angular/core/testing';

import { FactorService } from './factor.service';

describe('FactorService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [FactorService]
    });
  });

  it('should be created', inject([FactorService], (service: FactorService) => {
    expect(service).toBeTruthy();
  }));
});
