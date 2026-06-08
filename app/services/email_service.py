import os
import markdown
import resend
from datetime import datetime

resend.api_key = os.getenv(
    "RESEND_API_KEY"
)


def build_newsletter_html(newsletter):

    body_html = markdown.markdown(
        newsletter.content,
        extensions=["extra"]
    )
    
    today_date = datetime.now().strftime( "%B %d, %Y" )

    return f"""
    <html>
    <body
        style="
            font-family: Arial, sans-serif;
            padding: 40px;
            line-height: 1.6;
        "
    >

        <div
            style="
                max-width: 800px;
                margin: auto;
            "
        >

            <h2>
                THE AI DISPATCH
            </h2>
            
            <p style=" color: #6b7280; margin-top: 0; margin-bottom: 20px; font-size: 14px; " > {today_date} </p>

            <hr>

            {body_html}
            
            <hr> 
            
            <div style=" margin-top: 30px; text-align: center; " > 
            
            <p style=" color: #6b7280; font-size: 13px; " > 
            
            You're receiving this email because you subscribed to The AI Dispatch. </p> 
            
            <a href="http://localhost:8000/subscribers/unsubscribe" style=" display: inline-block; 
            padding: 10px 18px; border: 1px solid #d1d5db; border-radius: 6px; text-decoration: none; color: #374151; font-size: 14px; " > 
            Unsubscribe 
            </a> 
            
            </div>

        </div>

    </body>
    </html>
    """


def send_newsletter_email(
    email,
    newsletter
):

    try:

        html = build_newsletter_html(
            newsletter
        )

        response = resend.Emails.send(
            {
                "from": "AI Dispatch <newsletter@theaidispatch.in>",
                "to": [email],
                "subject": f"Newsletter: {newsletter.created_at.strftime('%B %d, %Y')}",
                "html": html
            }
        )

        print(
            f"Email sent successfully to {email}"
        )

        return {
            "success": True,
            "email": email,
            "response": response
        }

    except Exception as e:

        print(
            f"Failed to send email to {email}: {e}"
        )

        return {
            "success": False,
            "email": email,
            "error": str(e)
        }

def send_welcome_email(
    email
):

    try:

        html = """
        <html>
        <body
            style="
                font-family: Arial, sans-serif;
                line-height: 1.6;
                padding: 40px;
            "
        >

            <div
                style="
                    max-width: 700px;
                    margin: auto;
                "
            >

                <h1>
                    Welcome to The AI Dispatch
                </h1>

                <p>
                    Thanks for subscribing.
                </p>

                <p>
                    Every edition cuts through the noise and delivers
                    the AI stories actually worth your attention.
                </p>

                <hr>

                <h3>
                    What you'll receive:
                </h3>

                <ul>
                    <li>Breaking AI developments</li>
                    <li>Research and model releases</li>
                    <li>Industry news and funding</li>
                    <li>Concise summaries of important stories</li>
                </ul>

                <hr>

                <blockquote
                    style="
                        border-left: 4px solid #d1d5db;
                        padding-left: 16px;
                        color: #4b5563;
                    "
                >
                    The goal isn't to cover every AI story.
                    It's to cover the ones that matter.
                </blockquote>

                <p>
                    Your first edition will arrive soon.
                </p>

                <div
                    style="
                        margin: 30px 0;
                        text-align: center;
                    "
                >

                    <a
                        href="https://www.theaidispatch.in/newsletter"
                        style="
                            display: inline-block;
                            background: #111827;
                            color: #ffffff;
                            padding: 12px 24px;
                            border-radius: 6px;
                            text-decoration: none;
                            font-weight: 600;
                        "
                    >
                        Read The Latest Edition
                    </a>

                </div>

                <p>
                    — Daksh<br>
                    Founder, The AI Dispatch
                </p>

            </div>

        </body>
        </html>
        """

        response = resend.Emails.send(
            {
                "from": "AI Dispatch <newsletter@theaidispatch.in>",
                "to": [email],
                "subject": "You're in. Welcome to The AI Dispatch.",
                "html": html
            }
        )

        print(
            f"Welcome email sent to {email}"
        )

        return {
            "success": True,
            "email": email,
            "response": response
        }

    except Exception as e:

        print(
            f"Failed to send welcome email to {email}: {e}"
        )

        return {
            "success": False,
            "email": email,
            "error": str(e)
        }