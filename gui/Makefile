all: main_ui.py imdb_ui.py images_rc.py preferences_ui.py about_ui.py login_ui.py chooseLanguage_ui.py expiration_ui.py

main_ui.py : main.ui
	pyuic4 main.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// | python Qt2Po.py > main_ui.py

expiration_ui.py : expiration.ui
	pyuic4 expiration.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// > expiration_ui.py

login_ui.py : login.ui
	pyuic4 login.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// | python Qt2Po.py > login_ui.py
    
imdb_ui.py : imdb.ui
	pyuic4 imdb.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// | python Qt2Po.py > imdb_ui.py

preferences_ui.py : preferences.ui
	pyuic4 preferences.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// | python Qt2Po.py > preferences_ui.py

about_ui.py : about.ui
	pyuic4 about.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*// | python Qt2Po.py > about_ui.py

chooseLanguage_ui.py : chooseLanguage.ui
	pyuic4 chooseLanguage.ui | sed -s s/^.*Margin.*// | sed -e s/^.*boxlayout\.setObjectName.*//  > chooseLanguage_ui.py
    
images_rc.py : images.qrc
	pyrcc4 images.qrc > images_rc.py

clean :
	rm -f main_ui.py imdb_ui.py images_rc.py login_ui.py preferences_ui.py about_ui.py chooseLanguage_ui.py expiration_ui.py
