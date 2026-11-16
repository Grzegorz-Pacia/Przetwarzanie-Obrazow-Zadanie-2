from PIL import Image
import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.pyplot import figure
import numpy as np
import math

def main():

    #Wczytywanie obrazów zdalnych
    headers = {"User-Agent": "Mozilla/5.0 (grzegorz.pacia@student.wsb.edu.pl)"} #tworzy header dla User-Agenta potrzebnego do automatycznego pobierania obrazów z wikimedia
    images = [] #tworzy tablicę, która w liniach poniżej jest wypełniania kolejnymi obrazami zdalnymi
    images.append(Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/f/ff/Road%2C_Mary_Peters_Track%2C_Belfast_-_geograph.org.uk_-_2493800.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw))
    images.append(Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/2/26/Paharpur_image_by_Ruhan_1.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw))
    images.append(Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/5/51/Organo_Cripta_Monte.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw))
    images.append(Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/f/f9/Fog%2C_Belfast_City_Airport_%28January_2018%29_-_geograph.org.uk_-_5648768.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw))

    for image in images: #wykonuje program dla każdego z obrazów zdalnych

        #Wyświetlenie oryginalnego obrazu
        imageArray = np.asarray(image) #przetwarza obraz na array
        plt.imshow(imageArray, cmap=cm.gray, vmin=0, vmax=255) #przygotowuje obraz do wyświetlenia
        plt.title("Oryginalny obraz") #ustawia tytuł wyświetlanego obrazu
        plt.show() #wyświetla oryginalny obraz

        #Przetworzenie obrazu na grayscale
        imageGrayscale = image.convert("L") #zamienia obraz na grayscale
        imageGrayscaleArray = np.asarray(imageGrayscale) #przetwarza obraz grayscale na array

        #Przygotowanie tablic z kanałami kolorów obrazu
        imageRedArray = np.empty([len(imageArray), len(imageArray[0])], int) #przygotowuje tablicę dla każdego z kanałów kolorów oryginalnego obrazu
        imageGreenArray = np.empty([len(imageArray), len(imageArray[0])], int)
        imageBlueArray = np.empty([len(imageArray), len(imageArray[0])], int)
        for i in range (0, len(imageArray)): #wypełnia każdą z tablic wartościami dla danego kanału obrazu
            for j in range (0, len(imageArray[0])):
                imageRedArray[i][j] = imageArray[i][j][0]
                imageGreenArray[i][j] = imageArray[i][j][1]
                imageBlueArray[i][j] = imageArray[i][j][2]


        #Przygotowanie histogramów i ich wyświetlenie
        fig, ax = plt.subplots(2,2) #przygotowuje możliwość wyświetlenia czterech histogramów jednocześnie
        ax[0,0].hist(imageGrayscaleArray.flatten(), bins=256, range=[0, 256], color="gray") #przygotowuje kolejne histogramy do wyświetlenia
        ax[0,1].hist(imageRedArray.flatten(), bins=256, range=[0, 256], color="red")
        ax[1,0].hist(imageGreenArray.flatten(), bins=256, range=[0, 256], color="green")
        ax[1,1].hist(imageBlueArray.flatten(), bins=256, range=[0, 256], color="blue")

        histGray, binsGray = np.histogram(imageGrayscaleArray.flatten(), 256, [0, 256]) #przygotowuje odpowiednie histogramy do późniejszej analizy
        histRed, binsRed = np.histogram(imageRedArray.flatten(), 256, [0, 256])
        histGreen, binsGreen = np.histogram(imageGreenArray.flatten(), 256, [0, 256])
        histBlue, binsBlue = np.histogram(imageBlueArray.flatten(), 256, [0, 256])
        YLimit = max(max(histGray), max(histRed), max(histGreen), max(histBlue), 100) #znajduje najwyższą pojedynczą wartość ze wszystkich histogramów

        for i in range(0,2): #ustawia odpowiednie wymiary, umożliwiające łatwe porównanie histogramów
            for j in range(0,2):
                ax[i,j].set_ylim(0, YLimit)
                ax[i,j].set_xlim(0, 255)

        ax[0,0].set_title("Histogram - całe zdjęcie") #dodaje kolejne tytuły histogramów
        ax[0,1].set_title("Kanał czerwony")
        ax[1,0].set_title("Kanał zielony")
        ax[1,1].set_title("Kanał niebieski")
        fig.tight_layout() #ustawia prawidłowe rozmieszczenie histogramów w oknie
        plt.show() #wyświetla histogramy


        #Sprawdzenie, czy obraz jest prześwietlony lub niedoświetlony
        histogramRanges = [[0,50],[51,101],[102,153],[154,204],[205,255]] #5 zakresów histogramu obrazu, używanych do sprawdzania prześwietlenia i niedoświetlenia
        histogramValueArray = [0,0,0,0,0] #sumy wartości histogramu w powyższych zakresach
        for i in range(0,5): #sumuje wartości histogramu w powyższych zakresach
            for j in range(histogramRanges[i][0], histogramRanges[i][1]):
                histogramValueArray[i] += histGray[j]

        overExposed = False #jeśli True, obraz jest prześwietlony
        if(histogramValueArray[4]*2 + histogramValueArray[3] > histogramValueArray[2]*3): #sprawdza, czy obraz jest prześwietlony
            overExposed = True
        underExposed = False #jeśli True, obraz jest niedoświetlony
        if(histogramValueArray[0]*2 + histogramValueArray[1] > histogramValueArray[2]*3): #sprawdza, czy obraz jest niedoświetlony
            underExposed = True

        #Sprawdzenie, czy obraz ma niski kontrast, jeśli nie jest prześwietlony lub niedoświetlony
        lowContrast = False #jeśli True, kontrast obrazu jest niski
        if((not overExposed) and (not underExposed)):
            histogramSum = sum(histogramValueArray) #suma wszystkich wartości histogramu obrazu
            majorValuesStart = 0
            startSum = 0
            while(startSum < histogramSum*0.04): #znajduje wartość, na której wartość sumy wszystkich wartości histogramu (sumując od lewej) przekracza 4% całości sumy
                startSum += histGray[majorValuesStart]
                majorValuesStart+=1
            majorValuesEnd = 255
            endSum = histogramSum
            while(endSum > histogramSum*0.96): #znajduje wartość, na której wartość sumy wszystkich wartości histogramu (sumując od lewej) przekracza 96% całości sumy
                endSum -= histGray[majorValuesEnd]
                majorValuesEnd-=1
            if(majorValuesEnd - majorValuesStart < 75): #określa, na ilu z 256 wartości histogramu znajduje się 92% sumy jego wartości - jeśl zakres ten jest mniejszy niż 75, obraz zostaje określony jako mający niski kontrast
                lowContrast = True


        #Poprawianie prześwietlenia, niedoświetlenia lub kontrastu
        colorChannels = [imageRedArray, imageGreenArray, imageBlueArray] #umieszcza tablice z kanałami kolorów obrazu w tablicy
        enhancedImageArray = np.empty([len(imageArray), len(imageArray[0]), 3], int) #szykuje pustą tablicę na poprawiony obraz

        if(overExposed or underExposed): #jeśli obraz jest niedoświetlony lub prześwietlony
            if(underExposed): #jeśli obraz jest niedoświetlony
                for i in range (0, len(imageArray)):
                    for j in range (0, len(imageArray[0])):
                        for c in range(0,3):
                            color = colorChannels[c]
                            enhancedImageArray[i][j][c] = int(color[i][j]*(0.89+0.1*math.pow(1.0125, (255-color[i][j])))) #dla każdego z kanałów kolorów kolor nowego piksela jest określony tą formułą
            if(overExposed): #jeśli obraz jest prześwietlony
                for i in range (0, len(imageArray)):
                    for j in range (0, len(imageArray[0])):
                        for c in range(0,3):
                            color = colorChannels[c]
                            enhancedImageArray[i][j][c] = int(color[i][j]/(0.90+0.1*math.pow(1.0182, (255-color[i][j])))) #dla każdego z kanałów kolorów kolor nowego piksela jest określony tą formułą

        if(lowContrast): #jeśli obraz ma niski kontrast
            histogramCentralPoint = majorValuesStart + (majorValuesEnd - majorValuesStart)/2 #określa punkt będący środkiem 92% środkowych wartości histogramu
            for i in range (0, len(imageArray)):
                for j in range (0, len(imageArray[0])):
                    for c in range(0,3):
                        color = colorChannels[c]
                        enhancedImageArray[i][j][c] = int(2*(color[i][j]) - histogramCentralPoint) #dla każdego z kanałów kolorów kolor nowego piksela jest określony tą formułą
                        if(enhancedImageArray[i][j][c] < 0): enhancedImageArray[i][j][c] = 0 #dla bardzo niewielkiego zakresu kolorów może dojść do niewielkiej utraty szczegółowości
                        if(enhancedImageArray[i][j][c] > 255): enhancedImageArray[i][j][c] = 255


        #Wyświetlanie obrazu oryginalnego i poprawionego (jeśli oryginał był prawidłowy, jedynie oryginalnego)
        if((not overExposed) and (not underExposed) and (not lowContrast)): #jeśli obraz był prawidłowej jakości, wyświetla go
            plt.imshow(imageArray, cmap=cm.gray, vmin=0, vmax=255)
            plt.title("Obraz oryginalny - dobrej jakości")
            plt.show()
        else: #jeśli obraz został poprawiony
            fig2, ax2 = plt.subplots(1,2) #szykuje możliwość wyświetlenia dwóch obrazów jednocześnie
            ax2[0].imshow(imageArray, cmap=cm.gray, vmin=0, vmax=255) #przygotowuje oba obrazy do wyświetlenia
            ax2[1].imshow(enhancedImageArray, cmap=cm.gray, vmin=0, vmax=255)

            originalTitle = "Oryginał - " #przechowuje tytuł dla oryginalnego obrazu
            if (overExposed and underExposed): #dobiera odpowiedni tytuł dla oryginalnego obrazu
                originalTitle += "prześwietlony, niedoświetlony"
            elif (overExposed):
                originalTitle += "prześwietlony"
            elif (underExposed):
                originalTitle += "niedoświetlony"
            elif (lowContrast):
                originalTitle += "z niskim kontrastem"

            ax2[0].set_title(originalTitle) #nadaje tytuły obrazom
            ax2[1].set_title("Obraz poprawiony")
            fig2.tight_layout() #ustawia prawidłowe rozmieszczenie obrazów w oknie
            plt.show() #wyświetla obrazy
                

if __name__ == "__main__":
    main()