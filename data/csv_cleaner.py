import pandas as pd 

in_path = "./handm.csv"
df = pd.read_csv(in_path)

# drop unneeded columns
for c in df.columns:
    if(c == 'brandName'):
        df.drop(c, axis=1, inplace=True)
    if(c == 'stockState'):
        df.drop(c, axis=1, inplace=True)
    if(c == 'comingSoon'):
        df.drop(c, axis=1, inplace=True)
    if(c == 'isOnline'):
        df.drop(c, axis=1, inplace=True)
    if(c == 'newArrival'):
        df.drop(c, axis=1, inplace=True)
    if(c == 'materials'):
        df.drop(c, axis=1, inplace=True)


with open('sorted_types.txt', 'r') as file:
    array = [line.strip() for line in file.readlines()]
# print(array)

print("Search for types in CSV that are not in file:")
for i, p in enumerate(df['mainCatCode'].unique()):
    if p not in array:
        print(p)

print("Search for types in file that are not in CSV:")
for i, p in enumerate(array):
    if p not in df['mainCatCode'].unique():
        if p != '':
            print(p)

# # hand sorting and testing
# for i, p in enumerate(df['mainCatCode']):
#     if p == '[insert catcode here]':
#         print(df['url'][i])

# Calculate category counts for verification
mensTopCount = 0
mensBottomCount = 0
mensShoesCount = 0
mensOtherCount = 0
womensTopCount = 0
womensBottomCount = 0
womensShoesCount = 0
womensOtherCount = 0
type = 0
for i, p in enumerate(array):
    if p == '':
        type += 1
    else:
        if type == 0:
            mensTopCount += 1
        if type == 1:
            mensBottomCount += 1
        if type == 2:
            mensShoesCount += 1
        if type == 3:
            mensOtherCount += 1
        if type == 4:
            womensTopCount += 1
        if type == 5:
            womensBottomCount += 1
        if type == 6:
            womensShoesCount += 1
        if type == 7:
            womensOtherCount += 1

# print(mensTopCount)
# print(mensBottomCount)
# print(mensShoesCount)
# print(mensOtherCount)
# print(womensTopCount)
# print(womensBottomCount)
# print(womensShoesCount)
# print(womensOtherCount)

# print("index of '': ")
separations = []
for i, p in enumerate(array):
    if p == '':
        separations.append(i)
# print(separations)

---

# type = []
# for i, r in df.iterrows():
#     if array.index(r['mainCatCode']) >= 0 and array.index(r['mainCatCode']) < separations[0]:
#         type.append('mensTop')
#     elif array.index(r['mainCatCode']) >= separations[0] and array.index(r['mainCatCode']) < separations[1]:
#         type.append('mensBottom')
#     elif array.index(r['mainCatCode']) >= separations[1] and array.index(r['mainCatCode']) < separations[2]:
#         type.append('mensShoes')
#     elif array.index(r['mainCatCode']) >= separations[2] and array.index(r['mainCatCode']) < separations[3]:
#         type.append('mensOther')
#     elif array.index(r['mainCatCode']) >= separations[3] and array.index(r['mainCatCode']) < separations[4]:
#         type.append('womensTop')
#     elif array.index(r['mainCatCode']) >= separations[4] and array.index(r['mainCatCode']) < separations[5]:
#         type.append('womensBottom')
#     elif array.index(r['mainCatCode']) >= separations[5] and array.index(r['mainCatCode']) < separations[6]:
#         type.append('womensShoes')
#     elif array.index(r['mainCatCode']) >= separations[6]:
#         type.append('womensOther')

# df['type'] = type

# df.to_csv('cleaned_handm.csv', index=False)
# print("CSV cleaned!")