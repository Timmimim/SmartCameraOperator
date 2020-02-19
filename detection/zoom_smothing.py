"""
    führt eine exponentielle Glättung von Zeitreihendaten aus.
    Das Ergebnis sollte jeweils gespeichert und beim nächsten Aufruf als
    lastSmoothedValue übergeben werden.
    params:
            alpha                   float;  Glättungsfaktor
            lastSmoothedValue       float;  Ergebnis der vorigen Messung der Zeitreihe nach deren Glättung
            value                   float;  aktuelle Messung der Zeitreihe, die geglättet werden soll
"""
def exp_smoothing(alpha, lastSmoothedValue, value):

    smoothedValue = alpha * value + (1-alpha) * lastSmoothedValue

    return smoothedValue

"""
    führt eine doppelte exponentielle Glättung aus.
    params:
            alpha                       float; Glättungsfaktor
            lastDoubleSmoothedValue     float; Ergebnis der vorigen Messung der Zeitreihe nach deren doppleter Glättung
            smoothedValue               float; Ergebnis der Glättung der aktuellen Messung
"""
def doubled_exp_smoothing(alpha, lastDoubleSmoothedValue, smoothedValue):

    doubleSmoothedValue = alpha * smoothedValue + (1-alpha) * lastDoubleSmoothedValue

    return doubleSmoothedValue

"""
    empirisch zeigt sich, dass diese Berechnung die Zeitreihe sehr gut bestimmt.
    Ohne verfälscht eine doppelte Glättung das Ergebnis
    Quelle: https://de.wikibooks.org/wiki/Statistik:_Gl%C3%A4ttungsverfahren

    params:
            smoothedValue           float;  Glättung der aktuellen Messung
            doubleSmoothedValue     float;  doppelte Glättung der akutellen Messung

"""
def finsih_double_smoothing(smoothedValue, doubleSmoothedValue):

    return 2 * smoothedValue - doubleSmoothedValue

"""
    Zoom smoothing via exponential smoothing function (double smoothing currently used)
    params:
            array_of_four_tuples    Array;
            frame_count             int;
            weight                  float;  smoothingfactor (0<weight<1)
"""
def exp_zoom_smoothing(array_of_four_tuples, frame_count, weight):
    # x and y coordinates of a bounding boxes center
    # w and h are width and height of the BB

    # initialize some values (timeseries needs to start with values furthest backwards)
    # alternativ mit alle 0 initialisieren
    tuple = array_of_four_tuples[(frame_count+1) % len(array_of_four_tuples)]

    lastSmoothedX = tuple[0]
    lastSmoothedY = tuple[1]
    lastSmoothedW = tuple[2]
    lastSmoothedH = tuple[3]

    lastDoubleSmoothedX = tuple[0]
    lastDoubleSmoothedY = tuple[1]
    lastDoubleSmoothedW = tuple[2]
    lastDoubleSmoothedH = tuple[3]

    i = 0
    while i < len(array_of_four_tuples):
        tuple = array_of_four_tuples[(frame_count+i+1) % len(array_of_four_tuples)]
        lastSmoothedX = exp_smoothing(weight, lastSmoothedX, tuple[0])
        lastDoubleSmoothedX = doubled_exp_smoothing(weight,
                                                    lastDoubleSmoothedX,
                                                    lastSmoothedX)
        lastSmoothedY = exp_smoothing(weight, lastSmoothedY, tuple[1])
        lastDoubleSmoothedY = doubled_exp_smoothing(weight,
                                                    lastDoubleSmoothedY,
                                                    lastSmoothedY)
        lastSmoothedW = exp_smoothing(weight, lastSmoothedW, tuple[2])
        lastDoubleSmoothedW = doubled_exp_smoothing(weight,
                                                    lastDoubleSmoothedW,
                                                    lastSmoothedW)
        lastSmoothedH = exp_smoothing(weight, lastSmoothedH, tuple[3])
        lastDoubleSmoothedH = doubled_exp_smoothing(weight,
                                                        lastDoubleSmoothedH,
                                                        lastSmoothedH)
        i += 1

    x = finsih_double_smoothing(lastSmoothedX, lastDoubleSmoothedX)
    y = finsih_double_smoothing(lastSmoothedY, lastDoubleSmoothedY)
    w = finsih_double_smoothing(lastSmoothedW, lastDoubleSmoothedW)
    h = finsih_double_smoothing(lastSmoothedH, lastDoubleSmoothedH)

    # eventuell kein finish und stattdessen lastSmoothedValues verwenden (kein doublen)
    # je nach performance kann ein Teil zuvor als Mean berechnet werden und als "kopfelement"
    # in der exponentiellen Glättung verwendet werden. Aber das müssen wir testen.

    return int(x), int(y), int(w), int(h)
