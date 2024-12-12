import streamlit as st
import google.generativeai as genai

class YemekOneriSistemi:
    def __init__(self, gemini_api_key):  # Düzeltme: _init_ yerine __init__ kullanıldı
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

    def malzeme_sec(self):
        st.header("Malzeme Seçimi")
        malzemeler = ["un", "süt", "yumurta", "salça", "yağ", "soğan", "biber", "bamya", "tavuk", "balık", "et"]

        secili_malzemeler = st.multiselect(
            "Aşağıdaki malzemelerden 5 tanesini seçin:",
            malzemeler,
            max_selections=5  # Maksimum seçim sınırı eklendi
        )

        return secili_malzemeler

    def yemek_turu_sec(self):
        st.header("Yemek Türü ve Mutfak Seçimi")
        mutfak_turu = st.selectbox("Hangi mutfak türünü tercih ediyorsunuz?", ["Türk", "İtalyan", "Çin", "Hint", "Meksika"])
        yemek_turu = st.selectbox("Hangi tür yemek yapmak istiyorsunuz?", ["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Tatlı"])
        return mutfak_turu, yemek_turu

    def gemini_tarif_onerisi(self, kullanici_malzemeleri, mutfak_turu, yemek_turu):
        prompt = f"""
        Aşağıdaki bilgilere göre bir yemek tarifi oluşturun:
        Malzemeler: {', '.join(kullanici_malzemeleri)}
        Mutfak: {mutfak_turu}
        Yemek Türü: {yemek_turu}

        Tarifi adım adım yazın:
        1. Malzemelerin ölçülerini belirtin
        2. Adım adım pişirme talimatları verin
        3. Pişirme süresi ve zorluğunu belirtin
        4. Varsa püf noktalarını paylaşın
        5. Kaç kişilik olduğunu söyleyin

        Lütfen tarifi Türkçe olarak ve mutfak kültürüne uygun şekilde yazın.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Gemini API'den yanıt alınırken hata oluştu: {e}")
            return None

def main():
    st.set_page_config(page_title="Günlük Yemek Öneri Uygulaması", page_icon="🍲")

    st.title("🍽️ Günlük Yemek Öneri Uygulaması")

    gemini_api_key = "AIzaSyAD6351uf_16SFyiS1x4DyPaQlKKwojsYU"

    sistem = YemekOneriSistemi(gemini_api_key)

    kullanici_malzemeleri = sistem.malzeme_sec()
    mutfak_turu, yemek_turu = sistem.yemek_turu_sec()

    if st.button("Yemek Önerisi Al"):
        if len(kullanici_malzemeleri) < 5:
            st.warning("Lütfen 5 malzeme seçin.")
        else:
            st.subheader("Seçilen Malzemeler")
            st.write(", ".join(kullanici_malzemeleri))

            st.subheader("Yemek Tarifi Önerisi")
            tarif = sistem.gemini_tarif_onerisi(kullanici_malzemeleri, mutfak_turu, yemek_turu)

            if tarif:
                st.write(tarif)
            else:
                st.warning("Tarif alınırken bir hata oluştu.")

if __name__ == "__main__":
    main()
