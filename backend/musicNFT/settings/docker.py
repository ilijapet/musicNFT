if IN_DOCKER:
    print("Running in Docker mode....")
    assert MIDDLEWARE[:1] == [
        "django.middleware.security.SecurityMiddleware",
    ]
