
def test_healthcheck(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200