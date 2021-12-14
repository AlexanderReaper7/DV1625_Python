def heapify(arr, length, i):
    """heapifies"""
    largest = i
    left = 2*i+1
    right = 2*i+2
    if left < length and arr[largest] < arr[left]:
        largest = left
    if right < length and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        temp = arr[i]
        arr[i] = arr[largest]
        arr[largest] = temp
        heapify(arr, length, largest)

def heapsort(arr):
    """Uses the heap sort algo to sort an array of elements."""
    for i in range(len(arr)//2-1, -1, -1):
        heapify(arr, len(arr), i)
    for i in range(len(arr)-1, 0, -1):
        temp = arr[i]
        arr[i] = arr[0]
        arr[0] = temp
        heapify(arr, i, 0)
