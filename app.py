import streamlit as st
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(page_title="Advanced Web Crawler", layout="wide")

st.title("🌐 Advanced Web Crawler Bot")
st.write("Extract Full Web Links, Images, and Videos from any website instantly.")

# User inputs the target website
target_website = st.text_input("Enter Website URL:", "https://wikipedia.org")

if st.button("Start Advanced Crawl"):
    st.write("🔍 Scanning the website structure... please wait...")
    
    try:
        # Download the webpage
        req = urllib.request.Request(target_website, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = urllib.request.urlopen(req).read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Create 3 layout tabs on the webpage
        tab1, tab2, tab3 = st.tabs(["🔗 Full Web Links", "🖼️ Images (Pics)", "🎥 Videos"])
        
        # 1. EXTRACT FULL WEB LINKS
        with tab1:
            st.subheader("All Discovered Web Links")
            web_links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(target_website, href) # Converts relative links to full URLs
                if full_url.startswith('http'):
                    web_links.append(full_url)
            
            unique_links = list(set(web_links))
            st.success(f"Found {len(unique_links)} unique web links!")
            for link in unique_links:
                st.write(f"👉 [{link}]({link})")
                
        # 2. EXTRACT IMAGES (PICS)
        with tab2:
            st.subheader("All Discovered Images")
            img_links = []
            for img_tag in soup.find_all('img', src=True):
                src = img_tag['src']
                full_img_url = urljoin(target_website, src)
                img_links.append(full_img_url)
                
            unique_imgs = list(set(img_links))
            st.success(f"Found {len(unique_imgs)} images!")
            
            # Display them or show links
            for img in unique_imgs:
                st.write(f"📷 Image Link: [{img}]({img})")
                
        # 3. EXTRACT VIDEOS
        with tab3:
            st.subheader("All Discovered Videos")
            video_links = []
            # Find native HTML5 video tags
            for video_tag in soup.find_all('video'):
                if video_tag.get('src'):
                    video_links.append(urljoin(target_website, video_tag['src']))
                for source in video_tag.find_all('source', src=True):
                    video_links.append(urljoin(target_website, source['src']))
            
            # Find embedded videos like YouTube iframes
            for iframe_tag in soup.find_all('iframe', src=True):
                src = iframe_tag['src']
                if 'youtube' in src or 'vimeo' in src or 'video' in src:
                    video_links.append(urljoin(target_website, src))
                    
            unique_videos = list(set(video_links))
            if unique_videos:
                st.success(f"Found {len(unique_videos)} video elements!")
                for video in unique_videos:
                    st.write(f"🎬 Video Source: [{video}]({video})")
            else:
                st.info("No explicit video tracks or video iframes found on this specific page.")
                
    except Exception as e:
        st.error(f"Could not extract data. Error details: {e}")
