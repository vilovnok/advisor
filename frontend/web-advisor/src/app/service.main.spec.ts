import { TestBed } from '@angular/core/testing';

import { ServiceMain } from './service.main';

describe('ServiceService', () => {
  let service: ServiceMain;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServiceMain);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
