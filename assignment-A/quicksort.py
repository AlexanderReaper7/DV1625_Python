#   Lomuto partition scheme from wikipedia
#
# algorithm quicksort(A, lo, hi) is
#     if lo < hi then
#         p := partition(A, lo, hi)
#         quicksort(A, lo, p - 1)
#         quicksort(A, p + 1, hi)
#
# algorithm partition(A, lo, hi) is
#     pivot := A[hi]
#     i := lo
#     for j := lo to hi do
#         if A[j] < pivot then
#             swap A[i] with A[j]
#             i := i + 1
#     swap A[i] with A[hi]
#     return i

def partition(arr, low, high):
    """partitions"""
    pivot = arr[high]
    i = (low - 1)
    j = low
    while j <= (high- 1):
        if arr[j] < pivot:
            i += 1
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
        j += 1
    temp = arr[i + 1]
    arr[i + 1] = arr[high]
    arr[high] = temp
    return i + 1

def quicksort_recursive(arr, low, high):
    """Recursive part of the algo"""
    if low < high:
        p = partition(arr, low, high)
        quicksort_recursive(arr, low, p - 1)
        quicksort_recursive(arr, p + 1, high)

def quicksort(arr):
    """Uses the quicksort algo to sort an array of elements. entry point"""
    quicksort_recursive(arr, 0, len(arr) -1)
