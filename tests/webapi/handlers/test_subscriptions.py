"""Subscription handler tests."""

import uuid


async def test_post_subscription(web_client, infrastructure):
    """Check subscriptions posting handler."""
    response = await web_client.post(
        '/subscriptions/',
        json={
            'from_newsfeed_id': '124',
            'to_newsfeed_id': '123',
        },
    )

    assert response.status == 200
    data = await response.json()
    assert uuid.UUID(data['id'])

    subscription_storage = infrastructure.subscription_storage()
    subscriptions = await subscription_storage.get(to_newsfeed='123')
    assert len(subscriptions) == 1
    assert subscriptions[0]['from_newsfeed_id'] == '124'
    assert subscriptions[0]['to_newsfeed_id'] == '123'