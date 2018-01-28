import { WebcorreosPage } from './app.po';

describe('webcorreos App', function() {
  let page: WebcorreosPage;

  beforeEach(() => {
    page = new WebcorreosPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
