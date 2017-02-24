import requests
import logging

logger = logging.getLogger(__name__)


class Button(object):
    button_type = None

    def __init__(self):
        """
        Some templates as well as the persistent menu support buttons that
        can perform different kinds of actions:

        Args:
            button_type (str): URL Button type: 'web_url'.
            title (str): Button title. 20 character limit.
        """
        self.payload = {'type': self.button_type}


class UrlButton(Button):
    """
    URL Button. Can be used to open a webpage in the in-app browser.
    """
    button_type = 'web_url'

    def __init__(self, title, url, webview_height_ratio='full',
                 messenger_extensions=True):
        """
        Args:
            url (str): This URL is opened in a mobile browser when the button
                       is tapped.
            webview_height_ratio (str): Height of the Webview.
                       Valid values: 'compact', 'tall', 'full'.
            messenger_extensions (bool):
                       Must be true if using Messenger Extensions.
        """
        super().__init__()
        self.payload.update({
            'title': title,
            'url': url,
            'webview_height_ratio': webview_height_ratio,
            'messenger_extensions': messenger_extensions,
        })


class PostbackButton(Button):
    """
    Postback Button. Sends back developer-defined payload so you can
    perform an action or reply back.
    """
    button_type = 'postback'

    def __init__(self, title, payload):
        """
        Args:
            payload (str): This data will be sent back to your webhook.
                1000 character limit.
        """
        super().__init__()
        self.payload.update({'title': title, 'payload': payload})


class CallButton(Button):
    """
    Call Button. Dials a phone number when tapped.
    """
    button_type = 'phone_number'

    def __init__(self, title, payload):
        """
        Args:
            payload (str): Format must have "+" prefix followed by the country
                code, area code and local number. For example, +16505551234.
        """
        super().__init__()
        self.payload.update({'title': title, 'payload': payload})


class ShareButton(Button):
    """
    Share Button. Opens a share dialog in Messenger enabling people
    to share message bubbles with friends.
    """
    button_type = 'element_share'


class BuyButton(Button):
    """
    Buy Button. Opens a checkout dialog to enables purchases.
    """
    button_type = 'payment'

    def __init__(self, title, payload, payment_summary):
        """
        Args:
            payload (str): Developer defined metadata about the purchase.
            payment_summary (dict): Fields used in the checkout dialog.
        """
        super().__init__()
        self.payload.update({
            'title': title,
            'payload': payload,
            'payment_summary': payment_summary,
        })


class LogInButton(Button):
    """
    Log In button. Used in Account Linking flow intended
    to deliver page-scoped user id on web safely.
    """
    button_type = 'account_link'

    def __init__(self, url):
        """
        Args:
            url (str): Authentication callback URL. Must be using https protocol.
        """
        super().__init__()
        self.payload.update({'url': url})


class LogOutButton(Button):
    """
    Log Out button. Used in Account Linking flow intended
    to deliver page-scoped user id on web safely.
    """
    button_type = 'account_unlink'


class QuickReply(object):

    def __init__(self, content_type, title='', payload='', image_url=''):
        """
        If content_type is 'location', title and payload are not used.

        Args:
            content_type (str): 'text' or 'location'.
            title (str): Caption of button. Only if content_type is text.
                It has a 20 character limit, after that it gets truncated
            payload (str): Custom data that will be sent back to you via
                webhook. Only if content_type is text.
                It has a 1000 character limit.
            image_url (str): URL of image for text quick replies (optional).
                Image for image_url should be at least 24x24 and will be
                cropped and resized.
        """
        self.payload = {
            'content_type': content_type,
        }
        if content_type == 'text':
            if not title and payload:
                raise AttributeError('You should specify title and payload.')
            self.payload.update({'title': title, 'payload': payload})
        if image_url:
            self.payload.update({'image_url': image_url})


class MessengerBot(object):

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token

    def call_send_api(self, recipient_id, payload):
        payload.update({
            'recipient': {
                'id': recipient_id,
            }
        })
        base_url = 'https://graph.facebook.com/v2.6/me/messages'
        response = requests.post(
            '{}?access_token={}'.format(base_url, self.page_access_token),
            json=payload,
        )
        if response.status_code == 200:
            response_body = response.json()
        else:
            # TODO: Check Error Codes
            logger.error('Unable to send message. Status code: {}. {}'.format(
                response.status_code, response.json())
            )

    def sendMessage(self, recipient_id, message):
        """
        Send plain text messages.

        Args:
            recipient_id (int): Recipient ID.
            message (str): Must be UTF-8 and has a 640 character limit.
        """
        payload = {
            'message': {
                'text': message,
            }
        }
        self.call_send_api(recipient_id, payload)

    def sendAudio(self, recipient_id, url):
        """
        You can send sounds by uploading them or sharing a URL.

        Args:
            recipient_id (int): Recipient ID.
            url (str): URL of audio.
        """
        self.sendAttachment(recipient_id, 'audio', url)

    def sendFile(self, recipient_id, url):
        """
        You can send files by uploading them or sharing a URL.

        Args:
            recipient_id (int): Recipient ID.
            url (str): URL of file.
        """
        self.sendAttachment(recipient_id, 'file', url)

    def sendImage(self, recipient_id, url):
        """
        You can send images by uploading them or sharing a URL.
        Supported formats are jpg, png and gif.

        Args:
            recipient_id (int): Recipient ID.
            url (str): URL of image.
        """
        self.sendAttachment(recipient_id, 'image', url)

    def sendVideo(self, recipient_id, url):
        """
        You can send videos by uploading them or sharing a URL.

        Args:
            recipient_id (int): Recipient ID.
            url (str): URL of video binary.
        """
        self.sendAttachment(recipient_id, 'video', url)

    def sendAttachment(self, recipient_id, attachment_type, url):
        """
        You can send images by uploading them or sharing a URL.
        Supported formats are jpg, png and gif.

        Args:
            recipient_id (int): Recipient ID.
            attachment_type (str): 'image', 'file', 'audio' or 'video'.
            url (str): URL of attachment object.
        """
        payload = {
            'message': {
                'attachment': {
                    'type': attachment_type,
                    'payload': {
                        'url': url,
                    }
                }
            }
        }
        self.call_send_api(recipient_id, payload)

    def sendButton(self, recipient_id, message, buttons):
        """
        Send a text and buttons attachment to request input from the user.
        The buttons can open a URL, or make a back-end call to your webhook.

        Args:
            recipient_id (int): Recipient ID.
            message (str): UTF-8 encoded text of up to 640 characters that
                           appears the in main body.
            url (str): URL of attachment object.
            buttons (list): Button objects.
        """
        payload = {
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': message,
                        'buttons': buttons,
                    }
                }
            }
        }
        self.call_send_api(recipient_id, payload)

    def sendQuickReply(self, recipient_id, message, quick_replies):
        """
         Quick Replies appear prominently above the composer, with the keyboard
         less prominent. When a quick reply is tapped, the message is sent in
         the conversation with developer-defined metadata in the callback.
         Also, the buttons are dismissed preventing the issue where users
         could tap on buttons attached to old messages in a conversation.

        Args:
            recipient_id (int): Recipient ID.
            message (str): Message text.
            quick_replies (list): QuickReply objects.
        """
        payload = {
            'message': {
                'text': message,
                'quick_replies': quick_replies
            }
        }
        self.call_send_api(recipient_id, payload)

    def sendSenderAction(self, recipient_id, sender_action):
        """
        Set typing indicators or send read receipts,
        to let users know you are processing their request.
        Typing indicators are automatically turned off after 20 seconds.

        Args:
            recipient_id (int): Recipient ID.
            sender_action (str): Sender action.
                mark_seen - Mark last message as read
                typing_on - Turn typing indicators on
                typing_of - Turn typing indicators off
        """
        if sender_action not in ['mark_seen', 'typing_on', 'typing_of']:
            raise AttributeError('Unknown sender action.')
        payload = {'sender_action': sender_action}
        self.call_send_api(recipient_id, payload)
