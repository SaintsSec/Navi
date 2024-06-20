from cipher import Cipher

class PF(Cipher):
    
    name = 'Playfair'
    type = 'cipher'

    def encode(args):
        text = args.text
        key=args.key
        bogus='x'
        ignore='i'

        if (not text.isalpha()):
            return {'text': "Only alpha text accepted", 'success': False}
        if (not key.isalpha()):
            return {'text': "Key is not alphabetical", 'success': False}
        
        key=key.lower()
        text=text.lower()

        # creation of 5x5 key matrix
        key_mat=[
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','','']]

        alpha=[0]*26
        alpha[ord(ignore)-ord('a')]=1
        counter=0
        for ch in key:
            if(alpha[ord(ch)-ord('a')]==0):
                key_mat[counter//5][counter%5]=ch
                alpha[ord(ch)-ord('a')]='1'
                counter+=1

        alpha_index=0
        while(alpha_index<26):
            if(alpha[alpha_index]==0):
                alpha[alpha_index]=1
                key_mat[counter//5][counter%5]=chr(ord('a')+alpha_index)
                counter+=1
            alpha_index+=1

        # Creates pairs from the input 'text' string
        pairs=[]
        index=0
        while (index<len(text)):
            if (index<(len(text)-1)):
                if(text[index]==text[index+1]):
                    pairs+=[[text[index],bogus]]
                    index+=1
                else:
                    pairs+=[[text[index],text[index+1]]]
                    index+=2
            else:
                pairs+=[[text[index],bogus]]
                index+=1

        # encoding via key matrix
        output=''
        for i,j in pairs:
            for iter_r in range(5):
                for iter_c in range(5):
                    if(key_mat[iter_r][iter_c]==i):
                        r_i=iter_r
                        c_i=iter_c
                    if(key_mat[iter_r][iter_c]==j):
                        r_j=iter_r
                        c_j=iter_c
            if (r_i==r_j):
                output+=key_mat[r_i][(c_i+1)%5]+key_mat[r_j][(c_j+1)%5]
            elif (c_i==c_j):
                output+=key_mat[(r_i+1)%5][c_i]+key_mat[(r_j+1)%5][c_j]
            else:
                output+=(key_mat[r_i][c_j]+key_mat[r_j][c_i])

        return {'text': output, 'success': True}

    def decode(args):
        text = args.text
        key=args.key
        ignore='i'
        bogus='x'

        if (not text.isalpha()):
            return {'text': "Only alpha text accepted", 'success': False}
        if (len(text)%2!=0):
            return {'text': "Odd number of characters in text. Cannot be decrypted", 'success': False}
        if (not key.isalpha()):
            return {'text': "Key is not alphabetical", 'success': False}
        
        key=key.lower()
        text=text.lower()

        # creation of 5x5 key matrix
        key_mat=[
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','',''],
            ['','','','','']]

        alpha=[0]*26
        alpha[ord(ignore)-ord('a')]=1
        counter=0
        for ch in key:
            if(alpha[ord(ch)-ord('a')]==0):
                key_mat[counter//5][counter%5]=ch
                alpha[ord(ch)-ord('a')]='1'
                counter+=1

        alpha_index=0
        while(alpha_index<26):
            if(alpha[alpha_index]==0):
                alpha[alpha_index]=1
                key_mat[counter//5][counter%5]=chr(ord('a')+alpha_index)
                counter+=1
            alpha_index+=1
        
        # form pairs from string to be decoded
        pairs=[]
        index=0
        while (index<len(text)):
            pairs+=[[text[index],text[index+1]]]
            index+=2

        # decode the string
        output=''
        for i,j in pairs:
            for iter_r in range(5):
                for iter_c in range(5):
                    if(key_mat[iter_r][iter_c]==i):
                        r_i=iter_r
                        c_i=iter_c
                    if(key_mat[iter_r][iter_c]==j):
                        r_j=iter_r
                        c_j=iter_c
            if (r_i==r_j):
                output+=key_mat[r_i][(c_i-1)%5]+key_mat[r_j][(c_j-1)%5]
            elif (c_i==c_j):
                output+=key_mat[(r_i-1)%5][c_i]+key_mat[(r_j-1)%5][c_j]
            else:
                output+=key_mat[r_i][c_j]+key_mat[r_j][c_i]

        #remove the bogus character
        output=output.replace(bogus,'')

        return {'text': output, 'success': True}

    def print_options():
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -k / --key ------- shift key

        ### Examples
        python main.py pf -e -t 'hello' -k 'charles'
        python main.py pf -d -t 'csazcu' -k 'charles'

        Note: Default ignored character is 'i' and bogus/filler character is 'x'
        ''')
