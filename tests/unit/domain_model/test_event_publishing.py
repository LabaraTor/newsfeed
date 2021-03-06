"""Event publishing tests."""


async def test_event_publishing(app):
    """Check event publishing."""
    newsfeed_id = '123'

    event_dispatcher_service = app.domainmodel.event_dispatcher_service()
    event_processor_service = app.domainmodel.event_processor_service()

    await _process_event(
        event_dispatcher_service,
        event_processor_service,
        newsfeed_id=newsfeed_id,
        data={
            'event_data': 'some_data_1',
        },
    )
    await _process_event(
        event_dispatcher_service,
        event_processor_service,
        newsfeed_id=newsfeed_id,
        data={
            'event_data': 'some_data_2',
        },
    )

    event_repository = app.domainmodel.event_repository()
    events = await event_repository.get_by_newsfeed_id(newsfeed_id)
    assert events[0].data == {
        'event_data': 'some_data_2',
    }
    assert events[1].data == {
        'event_data': 'some_data_1',
    }


async def test_event_publishing_to_subscriber(app):
    """Check event publishing."""
    newsfeed_id = '123'
    subscriber_newsfeed_id = '124'

    subscription_service = app.domainmodel.subscription_service()
    await subscription_service.create_subscription(
        newsfeed_id=subscriber_newsfeed_id,
        to_newsfeed_id=newsfeed_id,
    )

    event_dispatcher_service = app.domainmodel.event_dispatcher_service()
    event_processor_service = app.domainmodel.event_processor_service()

    await _process_event(
        event_dispatcher_service,
        event_processor_service,
        newsfeed_id=newsfeed_id,
        data={
            'event_data': 'some_data_1',
        },
    )
    await _process_event(
        event_dispatcher_service,
        event_processor_service,
        newsfeed_id=newsfeed_id,
        data={
            'event_data': 'some_data_2',
        },
    )

    event_repository = app.domainmodel.event_repository()
    events = await event_repository.get_by_newsfeed_id(newsfeed_id)
    assert events[0].data == {
        'event_data': 'some_data_2',
    }
    assert events[1].data == {
        'event_data': 'some_data_1',
    }

    subscriber_events = await event_repository.get_by_newsfeed_id(subscriber_newsfeed_id)
    assert subscriber_events[0].data == {
        'event_data': 'some_data_2',
    }
    assert subscriber_events[1].data == {
        'event_data': 'some_data_1',
    }


async def _process_event(event_dispatcher_service, event_processor_service, newsfeed_id, data):
    await event_dispatcher_service.dispatch_new_event(
        newsfeed_id=newsfeed_id,
        data=data,
    )
    await event_processor_service.process_event()
