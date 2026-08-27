def create_author_and_book(client, auth_headers):
    author = client.post("/authors", json={"name": "J.R.R. Tolkien"}, headers=auth_headers).json()
    book = client.post(
        "/books",
        json={"title": "O Hobbit", "isbn": "9788595084759", "total_copies": 1, "author_id": author["id"]},
        headers=auth_headers,
    ).json()
    return book


def test_loan_lifecycle(client, auth_headers):
    book = create_author_and_book(client, auth_headers)
    member = client.post(
        "/members", json={"name": "Maria Silva", "email": "maria@example.com"}, headers=auth_headers
    ).json()

    loan_response = client.post(
        "/loans", json={"book_id": book["id"], "member_id": member["id"], "loan_days": 7}, headers=auth_headers
    )
    assert loan_response.status_code == 201
    loan = loan_response.json()
    assert loan["is_returned"] is False

    book_after = client.get(f"/books/{book['id']}").json()
    assert book_after["available_copies"] == 0


def test_cannot_loan_unavailable_book(client, auth_headers):
    book = create_author_and_book(client, auth_headers)
    member = client.post(
        "/members", json={"name": "João Souza", "email": "joao@example.com"}, headers=auth_headers
    ).json()

    client.post(
        "/loans", json={"book_id": book["id"], "member_id": member["id"]}, headers=auth_headers
    )
    second_attempt = client.post(
        "/loans", json={"book_id": book["id"], "member_id": member["id"]}, headers=auth_headers
    )
    assert second_attempt.status_code == 409


def test_return_loan(client, auth_headers):
    book = create_author_and_book(client, auth_headers)
    member = client.post(
        "/members", json={"name": "Ana Lima", "email": "ana@example.com"}, headers=auth_headers
    ).json()
    loan = client.post(
        "/loans", json={"book_id": book["id"], "member_id": member["id"]}, headers=auth_headers
    ).json()

    response = client.put(f"/loans/{loan['id']}/return", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_returned"] is True

    book_after = client.get(f"/books/{book['id']}").json()
    assert book_after["available_copies"] == 1
