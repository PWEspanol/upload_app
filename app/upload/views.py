from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from upload.gps_distance import gps_distance_between_coordinates

# Create your views here.

def some_view(request):
    context = {
        "form": UploadFileForm(),
    }
    if request.method == "POST":

        # Creating Upload to variable

        csv_file = request.FILES['file']

        if not csv_file.name.endswith(".csv"):
            messages.warning(request, "THIS IS NOT '.csv' EXTENSION")
            return HttpResponseRedirect(request.path_info)


        csv_file = request.FILES['file']
        
        filename = csv_file.name

        # Checking wheter uploading file has ".csv" format

        # if not filename.endswith(".csv"):
        #     messages.warning(request, "THIS IS NOT '.csv' EXTENSION")
        #     return HttpResponseRedirect(request.path_info)

        df = csv_file.read().decode("utf-8").split('\n')
        lines = []

        # Creating list with data
        for line in df:
            line = line.replace('\r', "")
            line = line.split(',')
            lines.append(line)

        # Checking whether the last few items of list are not emty
        for i in range(1,3):
            if len(lines[-3 + i]) < 3:
                lines.pop()

        # In order to working in pandas library there is a necesseary
        # to create DataFrame

        df = pd.DataFrame(columns=lines[0], data=lines[1:])

        # Creating another Dataframe to working with it
        # and deleting anomalies in it

        df_output = df

        # In ordedr to calculating maximum distance between 2
        #  places for a plane i have to mutiply time
        #  and plane's velocity


        for i in range(0, len(df.timestamp) - 1):
            FlightTime = float(int(df.timestamp[i + 1])) - float(int(df.timestamp[i]))
            
            MaximumPlaneDistance = FlightTime / 3600 * 950
            
            place_1 = [float(df.latitude[i]), float(df.longitude[i])]
            place_2 = [float(df.latitude[i + 1]), float(df.longitude[i + 1])]
            
            DistanceBetween2Coordinates = gps_distance_between_coordinates(place_1, place_2)
            
            if DistanceBetween2Coordinates >= MaximumPlaneDistance:
                df_output = df_output.drop(i + 1)


        # Outputing transformed file

        lines = df_output.to_records(index=False)

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{filename}-without-anomalies.csv"'},
        )

        writer = csv.writer(response)

        writer.writerow(df.columns)

        # Writing into new file

        for line in lines:
            writer.writerow(line)


        return response
    # Create the HttpResponse object with the appropriate CSV header.


    return render(request, 'upload/upload_page.html', context)