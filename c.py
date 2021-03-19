from flask import Flask, request
import numpy as np
import math
#import pandas as pd
import matplotlib.pyplot as plt, mpld3


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        operation = request.form['operation']
        number1 = float(request.form["number1"])
        number2 = float(request.form["number2"])
        number3 = float(request.form["number3"])
        number4 = float(request.form["number4"])
        k=number1
        m=number2
        dpratio=number3
        freq = number4
        if operation == "+":
            wn = np.power((k/m),0.5)
            fn = 1/(2*math.pi)*wn
            T = 1/fn
            cc = 2*m*wn
            c = cc*dpratio
            wd = wn*np.power((1-(dpratio*dpratio)),0.5)
            fn = 1/(2*math.pi)*wd
            q = 1/(2*dpratio)
            tr = 0
            plt.plot(wn,q,'+')
            plt.savefig('plot.png')
            result=(wn,fn,T,cc,c,wd,fn,q,tr,'plot.png')
            return '''
                <html>
                    <body>
                        <p>Natural frequency [wn] is: {result[0]}</p>
                        <p>Natural frequency [fn] is: {result[1]}</p>
                        <p>Period of oscilattion [T] is: {result[2]}</p>
                        <p>Critical damping [cc] is: {result[3]}</p>
                        <p>Damping factor [c] is: {result[4]}</p>
                        <p>Damped natural angular frequency [wd] is: {result[5]}</p>
                        <p>Damped natural frequency [fd] is: {result[6]}</p>
                        <p>Quality factor [Q] is: {result[7]}</p>
                        <p>Transmissiblity [TR] is: {result[8]}</p>
                        <img src=""{{"plot.png"}}">
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>

                '''.format(result=result)

        elif operation == "-":
            #freq=float(input())
            freq=freq*2*math.pi
            wn = np.power((k/m),0.5)
            fn = 1/(2*math.pi)*wn
            T = 1/fn
            cc = 2*m*wn
            c = cc*dpratio
            wd = wn*np.power((1-(dpratio*dpratio)),0.5)
            fn = 1/(2*math.pi)*wd
            q = 1/(2*dpratio)
            a = 1+(np.power(2*dpratio*freq/wn,2))
            b = np.power((1-(np.power((freq/wn),2))),2)
            c1 = np.power(2*dpratio*freq/wn,2)
            tr = np.power(a/(b+c1),0.5)
            freq1=[]
            tr1=[]
            freq3 = 0
            freqratio = int(freq/fn)
            for i in range(1,freqratio):
                freqratio=freq3/wn
                freq1.append(freqratio)
                a = 1+(np.power(2*dpratio*freq3/wn,2))
                b = np.power((1-(np.power((freq3/wn),2))),2)
                c1 = np.power(2*dpratio*freq3/wn,2)
                tr2 = np.power(a/(b+c1),0.5)
                tr1.append(tr2)
                freq3 = 0.01+freq3
            fig, ax = plt.subplots()
            ax.loglog(freq1, tr1)
            plt.grid()
            #ax.loglog(freq,tr,'+')
            plt.title('Transmissiblity vs Frequency Ratio Graph(log-log)')
            plt.xlabel('Frequency Ratio')
            plt.ylabel('Transmissiblity [TR]')
            html_text = mpld3.fig_to_html(fig)
            result=(wn,fn,T,cc,c,wd,fn,q,tr,html_text)
            #result=(wn,fn,T,cc,c,wd,fn,q,tr)
            return '''
                    <html>
                        <body>
                            <p>Natural frequency [wn] is: {result[0]}</p>
                            <p>Natural frequency [fn] is: {result[1]}</p>
                            <p>Period of oscilattion [T] is: {result[2]}</p>
                            <p>Critical damping [cc] is: {result[3]}</p>
                            <p>Damping factor [c] is: {result[4]}</p>
                            <p>Damped natural angular frequency [wd] is: {result[5]}</p>
                            <p>Damped natural frequency [fd] is: {result[6]}</p>
                            <p>Quality factor [Q] is: {result[7]}</p>
                            <p>Transmissiblity [TR] is: {result[8]}</p>
                            <p><a href="/">Click here to calculate again</a>
                            {result[9]}
                            </body>
                            </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
                {errors}
                <h1>SINGLE DEGREE OF FREEDOM SYSTEMS (SDOF) - VIBRATION CALCULATOR</h1>
                <br/>

                <form method="post" action=".">
                    <label for="operation"><h3>Operation:</h3></label>
                    <select id="operation" name="operation">
                    <option value="+"><h4>Free Vibration-></h4></option>
                    <option value="-"><h4>Forced Vibration-></h4></option>

                    </select>
                    <br/>
                    <br/>
                    <br/>
                    <label for="number1">Mass [m] (in kg) :....................................</label>
                    <input type="text" name="number1" id="number1">
                    <br/>
                    <br/>
                    <label for="number2">k (in N/m) :..............................................</label>
                    <input type="text" name="number2" id="number2">
                    <br/>
                    <br/>
                    <label for="number3">Damping raito (coefficient) [ζ] :..............     </label>
                    <input type="text" name="number3" id="number3">
                    <br/>
                    <br/>
                    <label for="number4">Harmonic input frequency [Ω] (in Hz) :...</label>
                    <input type="text" name="number4" id="number4">
                    <br/>
                    (Enter 0 if it is free vibration)
                    <br/>
                    <br/>
                    <br/>
                    <input type="submit" value="Submit"/>
                    <input type="reset"  value="RESET" style="color: red;"/>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

if __name__ == '__main__':
    app.debug = True
    app.run()

