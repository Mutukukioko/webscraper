import csv

from django.http import HttpResponse


def emails_to_csv_response(emails):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="emails.csv"'
    writer = csv.writer(response)
    writer.writerow(["email", "url"])
    for email in emails:
        writer.writerow([email.email, email.url])
    return response
