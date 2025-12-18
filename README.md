
# Tapo Control

An application to control Tapo smart devices.

## Environment Setup

To use this project, you need to configure your environment variables.

1. Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```

2. Fill in the following values in your `.env` file:
    - **Account ID**: Your Tapo account username/email
    - **Password**: Your Tapo account password
    - **Device IP**: The IP address of your Tapo device

Example `.env`:
```
REACT_APP_TAPO_ACCOUNT_ID=your_email@example.com
REACT_APP_TAPO_PASSWORD=your_password
REACT_APP_TAPO_DEVICE_IP=192.168.1.100
```

## Future Improvements

Automatic device IP address discovery will be implemented in a future release.
Replace the opening description with:

## Going Further

we can try to add all the brands in one script be it tapo or philips or anything else.