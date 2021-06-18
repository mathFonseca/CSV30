// Exemplo: manipulando imagens com OpenCV (vers�o C++).

#include <time.h>
#include <iostream>
#include "opencv2/imgproc/imgproc.hpp" // O m�dulo imgproc cont�m fun��es gerais para processamento de imagens.
#include "opencv2/highgui/highgui.hpp" // O m�dulo highgui cont�m fun��es b�sicas para I/O e apresenta��o de resultados.

#define IN_IMG "teste.jpg"

using namespace cv; // Namespace do OpenCV.
using namespace std;

int main ()
{
	// A classe Mat � usada para representar imagens e matrizes.
	// Ela tem um vetor de dados interno, que � desalocado automaticamente pelo destruidor da classe.
	// A fun��o imread carrega uma imagem de um arquivo, alocando e preenchendo o vetor de dados.
	// Ela tem um segundo par�metro opcional que indica o n�mero de canais da imagem.
	// O valor default � CV_LOAD_IMAGE_COLOR, que l� as imagens com 3 canais (BGR).
	// Se o par�metro for mudado para CV_LOAD_IMAGE_GRAYSCALE, a imagem � carregada em escala de cinza (1 canal).
	Mat img = imread (IN_IMG);
	if (!img.data) // Se falhar, img.data == NULL.
	{
		cerr << "Nao conseguiu ler " << IN_IMG << ".\n";
		return (1);
	}

	// Convertendo para float32. Dependendo da sequ�ncia de opera��es, e recomend�vel fazer esta convers�o (mas nem sempre � necessario).
	img.convertTo (img, CV_32F, 1.0/255.0);

	// Para exemplificar a forma de acesso aos dados da imagem, vamos criar uma vers�o em escala de cinza dela. A conta �:
	//
	// cinza = 0.299r + 0.587g + 0.114b
	//
	// Lembrando que a ordem dos canais na imagem colorida � (B, G, R).
	// Faremos isso tr�s vezes, para comparar o desempenho.
	Mat img_gs (img.rows, img.cols, CV_32FC1); // CV_32FC1 = float32, 1 canal.

	// Vers�o 1: usando a fun��o at. Esta opera��o � lenta, e deve ser evitada quando possivel. Otimiza��es do compilador podem melhorar isso, mas n�o totalmente.
	clock_t start_time = clock ();
	for (int row = 0; row < img.rows; row++)
		for (int col = 0; col < img.cols; col++)
		{
			Vec3f pixel = img.at <Vec3f> (row, col); // Vec3f: 3-tupla de float32.
			img_gs.at <float> (row, col) = pixel [0]*0.114f + pixel [1]*0.587f + pixel [2]*0.299f;
		}
	cout << "Tempo com at: " << clock () - start_time << endl;

	// Vers�o 2: usando ponteiros. Quando for percorrer uma imagem pixel a pixel, fa�a sempre assim.
	start_time = clock ();
	int rows = img.rows;
	int cols = img.cols;
	if (img.isContinuous () && img_gs.isContinuous ()) // Truque: se o buffer for cont�nuo, coloca tudo em uma linha gigante.
	{
		cols *= rows;
		rows = 1;
	}

	for (int row = 0; row < rows; row++)
	{
		float* ptr_in = (float*) (img.data + row*img.step); // Posiciona o ponteiro no in�cio da linha atual.
		float* ptr_out = (float*) (img_gs.data + row*img_gs.step);
		for (int col = 0; col < cols; col++)
		{
			*ptr_out = ptr_in [0]*0.114f + ptr_in [1]*0.587f + ptr_in [2]*0.299f;
			ptr_in += 3; // Pula 3 posi��es (3 canais).
			ptr_out++; // Pula 1 posi��o.
		}
	}
	cout << "Tempo com ponteiros: " << clock () - start_time << endl;

	// Vers�o 3: usando a fun��o embutida do OpenCV.
	start_time = clock ();
	cvtColor (img, img_gs, COLOR_BGR2GRAY);
	cout << "Tempo OpenCV: " << clock () - start_time << endl;

	// Mostra os resultados.
	imshow ("cor", img);
	imshow ("cinza", img_gs);

	// Salva. Note que eu preciso multiplicar de novo por 255, mas n�o preciso reconverter para inteiro.
	imwrite ("cinza.png", img_gs * 255);

	// A fun��o waitKey fica esperando o usu�rio pressionar uma tecla.
	// Ela recebe um par�metro, com valor default 0, que diz quantos milissegundos a fun��o espera - se o valor for menor ou igual a 0, a fun��o espera indefinidamente.
	// O valor de retorno � o c�digo ASCII da tecla pressionada - neste caso, n�o importa.
	// Experimente mudar o par�metro para 1000 para ver o que acontece.
	waitKey ();

	destroyAllWindows ();
	return (0);
}