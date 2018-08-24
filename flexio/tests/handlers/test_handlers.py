class TestHandlers(object):
    def test_404(self, client):
        response = client.get('https://www.foo.bar.bar.foo.page.not.found')
        data = str(response.data)
        assert response.status_code == 404
        assert "fa-exclamation" in data
