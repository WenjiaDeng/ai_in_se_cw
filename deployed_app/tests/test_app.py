from app import app


def test_homepage_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_adddata_route_exists():
    rules = [str(rule) for rule in app.url_map.iter_rules()]
    assert "/adddata" in rules


def test_dishes_route_exists():
    rules = [str(rule) for rule in app.url_map.iter_rules()]
    assert "/dishes" in rules


def test_orders_route_exists():
    rules = [str(rule) for rule in app.url_map.iter_rules()]
    assert "/orders" in rules