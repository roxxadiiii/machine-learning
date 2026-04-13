art = '''
╔═╗ ┬ ┬┬┌─┐┬┌─╔═╗┌─┐┬─┐┌┬┐
║═╬╗│ │││  ├┴┐╚═╗│ │├┬┘ │ 
╚═╝╚└─┘┴└─┘┴ ┴╚═╝└─┘┴└─ ┴

GITHUB/CODEBERG - @roxxadiiii
''' 

psudoCode = '''
int partition(arr,low,high){
    pivot = arr[low];
    i = low;
    j = high;

    while(i<j){
        while(arr[i] <= arr[pivot] && i <= high-1){
        i++;
        }

        while(arr[j] > arr[pivot] && j >= low+1){
            j--;
        }
        if(i < j){
            swap(arr[i],arr[j])
        }
    }
    swap(arr[low],arr[j]);
    return j;
}


quickSort(arr,low,high){
    if(low<high){
        int pIndex = partition(arr,low,high);
        quickSort(arr,low,pIndex-1);
        quickSort(arr,pIndex+1,high)
    }

}

'''


# code in python

# fun for the parition index 

def partition(arr , low , high):
    pivot = arr[low]

    i = low
    j = high

    while i < j:
        while i <= high - 1 and arr[i] <= pivot:
            i = i + 1
        while j >= low + 1 and arr[j] > pivot:
            j = j - 1

        if i < j:
            arr[i],arr[j] = arr[j],arr[i]
    arr[low],arr[j] = arr[j] , arr[low]

    return j

# function for quickSort

def quickSort(arr , low , high):
    if low < high:
        pIndex = partition(arr , low , high)

        quickSort(arr , low , pIndex - 1)

        quickSort(arr , pIndex + 1 , high)

print(art)
# print(psudoCode) # remove the comment for psudo code

arr = list(map(int,input("ENTER THE ARRAY ELEMENTS (seprate with space) : ").split()))
quickSort(arr, 0, len(arr) - 1)
print("Sorted Array are : ", arr)


print("SCRIPT ended......")
print("Run it again")
