def test_onboarding_and_chat_flow(client):
    payload = {
        "name": "Asha",
        "email": "asha@example.com",
        "experience_level": "beginner",
        "programming_knowledge": "basic Python",
        "problem_solving_confidence": 3,
        "goal": "placement preparation",
        "preferred_language": "Python",
        "preferred_learning_style": "guided examples",
    }
    created = client.post("/api/onboarding", json=payload)
    assert created.status_code == 200
    student_id = created.json()["student"]["id"]

    response = client.post("/api/chat", json={"student_id": student_id, "question": "What is Binary Search?", "topic": "Binary Search"})
    assert response.status_code == 200
    body = response.json()
    assert body["student_id"] == student_id
    assert len(body["guiding_questions"]) == 2


def test_code_analysis(client):
    created = client.post(
        "/api/onboarding",
        json={
            "name": "Dev",
            "email": "dev@example.com",
            "experience_level": "intermediate",
            "programming_knowledge": "Python projects",
            "problem_solving_confidence": 4,
            "goal": "DSA",
            "preferred_language": "Python",
        },
    )
    student_id = created.json()["student"]["id"]
    response = client.post("/api/analyze", json={"student_id": student_id, "language": "python", "code": "for i in range(3)\n print(i)", "topic": "Loops"})
    assert response.status_code == 200
    assert response.json()["findings"]
