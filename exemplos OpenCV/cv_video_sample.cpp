// Exemplo: manipulando v�deos com OpenCV (vers�o C++).

#include <iostream>
#include "opencv2/imgproc/imgproc.hpp" // O m�dulo imgproc cont�m fun��es gerais para processamento de imagens.
#include "opencv2/highgui/highgui.hpp" // O m�dulo highgui cont�m fun��es b�sicas para I/O e apresenta��o de resultados.

#define ESC_KEY 27 // C�digo da tecla ESC.
#define IN_VIDEO 0 // O v�deo de entrada pode ser um n�mero ou um nome de arquivo. Se for um n�mero, o programa tentar� abrir a c�mera com o n�mero dado.

using namespace std;
using namespace cv; // Namespace do OpenCV.

int main ()
{
	VideoCapture in_video (IN_VIDEO);

	// Se o v�deo vier da webcam, podemos tentar definir a resolu��o (depende da c�mera).
	if (IN_VIDEO == 0)
	{
		in_video.set (CAP_PROP_FRAME_WIDTH, 1280);
		in_video.set (CAP_PROP_FRAME_HEIGHT, 720);
	}

	if (!in_video.isOpened ())
	{
		cerr << "Nao conseguiu usar a webcam." << endl;
		return (1);
	}

	// Pega a resolu��o do video.
	int rows = int (in_video.get (CAP_PROP_FRAME_HEIGHT));
	int cols = int (in_video.get (CAP_PROP_FRAME_WIDTH));

	// O FourCC � um c�digo de 4 caracteres que identifica um codec de v�deo.
	// Os formatos v�lidos dependem dos codecs que est�o instalados no computador!
	int fourcc = VideoWriter::fourcc ('x','v','i','d');

	// Vamos salvar uma c�pia do video.
	VideoWriter out_video ("out.avi", fourcc, 30, Size (cols, rows), 1);
	if (!out_video.isOpened ())
	{
		cerr << "Nao conseguiu abrir o arquivo para escrita!\n";
		return (1);
	}

	// Um buffer qualquer.
	Mat img_gs (rows, cols, CV_8UC1);

	// Vai abrindo frames enquanto estiverem dispon�veis E enquanto a tecla ESC n�o for pressionada.
	char key = 0;
	Mat img;
	in_video.read (img);
	while (img.data && key != ESC_KEY)
	{
		cvtColor (img, img_gs, COLOR_BGR2GRAY);

		imshow ("cor", img);
		imshow ("cinza", img);

		out_video.write (img); // Salva o frame.
		in_video.read (img); // L� o pr�ximo frame.

		key = waitKey (1000/30); // Para manter ~30 fps.
	}
	
	in_video.release (); // Fecha os v�deos.
	out_video.release ();
	destroyAllWindows ();
	return (0);
}
