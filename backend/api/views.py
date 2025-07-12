# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import bcchapi
from datetime import datetime

@api_view(["GET"])
def indicadores_banco_central(request):
    """
    Endpoint para obtener indicadores del Banco Central de Chile
    """
    try:
        siete = bcchapi.Siete(file="credenciales.txt")

        series = {
            "dolar": "F073.TCO.PRE.Z.D",
            "uf": "F073.UFF.PRE.Z.D",
            "utm": "F073.UTR.PRE.Z.M",
            "euro": "F072.CLP.EUR.N.O.D",
            "yen": "F072.CLP.JPY.N.O.D",
            "ipc": "F074.IPC.VAR.Z.Z.C.M",
            "ivp": "F034.IPV.FLU.BCCH.2002.0.T",
            "imacec": "F032.IMC.IND.Z.Z.EP18.Z.Z.0.M",
            "tpm": "F022.TPM.TIN.D001.NO.Z.M",
            "libra_cobre": "F019.PPB.PRE.40.M",
            "tasa_desempleo": "F049.DES.TAS.INE9.10.M",
            "indice_remuneraciones": "F049.RMU.IND.HIST.81.M",
        }

        # Fechas
        desde = request.GET.get("desde", "2024-06-01")
        hasta = request.GET.get("hasta", datetime.today().strftime("%Y-%m-%d"))

        data = []

        for nombre, serie_id in series.items():
            try:
                df = siete.cuadro(
                    series=[serie_id],
                    nombres=[nombre],
                    desde=desde,
                    hasta=hasta,
                    observado={nombre: "last"},
                )
                ultimo_valor = df[nombre].dropna().iloc[-1]
                ultima_fecha = df.index[-1].strftime("%Y-%m-%d")

                data.append({
                    "codigo": nombre,
                    "nombre": nombre.upper(),
                    "valor": float(ultimo_valor),
                    "fecha": ultima_fecha,
                })
            except Exception as e:
                print(f"Error al obtener {nombre}: {e}")

        response = {
            "fecha": datetime.today().strftime("%Y-%m-%d"),
        }
        for item in data:
            response[item["codigo"]] = {
                "valor": item["valor"],
                "nombre": item["nombre"],
                "unidad_medida": "$" if item["codigo"] in ["dolar", "uf", "utm", "euro", "yen"] else "%"
            }

        return Response(response)
    
    except Exception as e:
        # Datos de fallback en caso de error
        return Response({
            "fecha": datetime.today().strftime("%Y-%m-%d"),
            "dolar": {"valor": 980.50, "nombre": "DOLAR", "unidad_medida": "$"},
            "uf": {"valor": 37500.00, "nombre": "UF", "unidad_medida": "$"},
            "utm": {"valor": 65967.00, "nombre": "UTM", "unidad_medida": "$"},
            "euro": {"valor": 1020.30, "nombre": "EURO", "unidad_medida": "$"},
            "error": f"Usando datos de respaldo: {str(e)}"
        })